from typing import List, Dict, Tuple
import logging
import time
from PyQt5 import QtCore

from network_variables import BufferedVariable
import clb_tests_base
import utils


class TestResults:
    def __init__(self):
        self.statuses = []
        self.variables_to_graph = {}
        self.__graph_data = []
        self.graph_normalize_time_value = 0

    def set_current_result_status(self, a_status: clb_tests_base.ClbTest.Status):
        self.statuses[-1] = a_status

    def new_result(self):
        self.statuses.append(clb_tests_base.ClbTest.Status.NOT_CHECKED)
        if self.variables_to_graph:
            self.__graph_data.append({name: ([], []) for name in self.variables_to_graph.keys()})

    def delete_results(self):
        self.statuses = []
        self.variables_to_graph = {}
        self.__graph_data = []

    def get_final_status(self) -> clb_tests_base.ClbTest.Status:
        assert self.statuses, "Ни одного результата не создано!!"

        if self.statuses[0] == clb_tests_base.ClbTest.Status.NOT_CHECKED:
            return clb_tests_base.ClbTest.Status.NOT_CHECKED

        for status in self.statuses:
            assert status != (clb_tests_base.ClbTest.Status.IN_PROCESS, clb_tests_base.ClbTest.Status.NOT_CHECKED)
            if status == clb_tests_base.ClbTest.Status.FAIL:
                return clb_tests_base.ClbTest.Status.FAIL
        return clb_tests_base.ClbTest.Status.SUCCESS

    def get_results_count(self) -> int:
        return len(self.statuses)

    def get_success_results_count(self) -> int:
        return self.statuses.count(clb_tests_base.ClbTest.Status.SUCCESS)

    def get_graph_data(self) -> List[Dict[str, Tuple[List[float], List[float]]]]:
        return self.__graph_data

    def set_variables_to_graph(self, a_variables_to_graph: Dict[str, BufferedVariable]):
        self.variables_to_graph = a_variables_to_graph

    def read_variables_to_graph(self):
        timestamp = time.time()

        for variable in self.variables_to_graph.keys():
            value = self.variables_to_graph[variable].get()
            current_graph = self.__graph_data[-1][variable]

            if not current_graph[0]:
                self.graph_normalize_time_value = timestamp
            # Список X-ов
            current_graph[0].append(round(timestamp - self.graph_normalize_time_value, 3))
            # Список Y-ов
            current_graph[1].append(value)

    def __str__(self):
        return f"{self.statuses}\n{self.__graph_data}"


class TestsConductor(QtCore.QObject):
    test_status_changed = QtCore.pyqtSignal(str, str, clb_tests_base.ClbTest.Status, int)
    graphs_have_been_updated = QtCore.pyqtSignal()
    tests_done = QtCore.pyqtSignal()

    def __init__(self, a_tests: List[clb_tests_base.ClbTest]):
        super().__init__()

        self.tests = a_tests
        self.test_results = [TestResults() for i in range(len(self.tests))]

        self.enabled_tests = []
        self.prepare_timer = utils.Timer(1.5)
        self.timeout_timer = utils.Timer(30)

        # Работает в цикличном режиме
        self.read_graphs_time = utils.Timer(0.5)
        self.read_graphs_time.start()

        self.__started = False
        self.current_test_idx = 0

    def set_enabled_tests(self, a_enabled_tests: List[int]):
        self.enabled_tests = a_enabled_tests

    def start(self):
        self.current_test_idx = 0
        if self.find_enabled_test():
            self.__started = True
            self.next_test(a_first_test=True)
        else:
            self.stop()
            self.tests_done.emit()

    def stop(self):
        if self.current_test_idx < len(self.tests):
            # Если тест прервали до его окончания
            self.tests[self.current_test_idx].stop()
            self.test_status_changed.emit(self.tests[self.current_test_idx].group(),
                                          self.tests[self.current_test_idx].name(),
                                          self.test_results[self.current_test_idx].get_final_status(),
                                          self.test_results[self.current_test_idx].get_success_results_count())

        self.__started = False
        self.current_test_idx = 0
        self.prepare_timer.stop()
        self.timeout_timer.stop()

    def find_enabled_test(self):
        if self.current_test_idx >= len(self.tests):
            return False

        while not (self.enabled_tests[self.current_test_idx] > 0):
            self.current_test_idx += 1

            if self.current_test_idx >= len(self.tests):
                return False

        return True

    def next_test(self, a_first_test):
        try:
            reset_status = False
            if not a_first_test:
                if self.enabled_tests[self.current_test_idx] <= 0:
                    self.test_status_changed.emit(self.tests[self.current_test_idx].group(),
                                                  self.tests[self.current_test_idx].name(),
                                                  self.test_results[self.current_test_idx].get_final_status(),
                                                  self.test_results[self.current_test_idx].get_success_results_count())
                    self.current_test_idx += 1
                    reset_status = True
            else:
                reset_status = True

            if self.find_enabled_test():
                self.enabled_tests[self.current_test_idx] -= 1
                current_test = self.tests[self.current_test_idx]
                current_results = self.test_results[self.current_test_idx]
                logging.info(f"----------------------------------------------------")
                logging.info(f'ТЕСТ "{current_test.group()}: {current_test.name()}" старт')
                self.prepare_timer.start()
                self.timeout_timer.start(current_test.timeout())

                if reset_status:
                    current_results.delete_results()
                    current_results.set_variables_to_graph(current_test.get_variables_to_graph())

                current_results.new_result()

                self.test_status_changed.emit(current_test.group(), current_test.name(),
                                              clb_tests_base.ClbTest.Status.IN_PROCESS,
                                              current_results.get_success_results_count())
            else:
                self.stop()
                self.tests_done.emit()
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def tick(self):
        if self.__started:
            current_test = self.tests[self.current_test_idx]
            current_results = self.test_results[self.current_test_idx]

            if not self.timeout_timer.check():
                if current_test.status() == clb_tests_base.ClbTest.Status.NOT_CHECKED:
                    if self.prepare_timer.check():
                        if current_test.prepare():
                            logging.info(f"Успешная подготовка")
                            current_test.start()
                        else:
                            self.prepare_timer.start()

                elif current_test.status() == clb_tests_base.ClbTest.Status.IN_PROCESS:
                    current_test.tick()

                    if self.read_graphs_time.check():
                        self.read_graphs_time.start()
                        current_results.read_variables_to_graph()
                        self.graphs_have_been_updated.emit()

                elif current_test.status() in (clb_tests_base.ClbTest.Status.SUCCESS,
                                               clb_tests_base.ClbTest.Status.FAIL):
                    logging.info(f'ТЕСТ "{current_test.group()}: {current_test.name()}" '
                                 f'результат {current_test.status().name}')
                    if current_test.has_error():
                        logging.warning(f'ТЕСТ "{current_test.group()}: {current_test.name()}" ' 
                                        f'Ошибка: {current_test.get_last_error()}')

                    current_results.set_current_result_status(current_test.status())
                    current_test.stop()
                    self.next_test(a_first_test=False)
            else:
                logging.warning(f'ТЕСТ "{current_test.group()}: {current_test.name()}" TIMEOUT')
                if current_test.has_error():
                    logging.warning(f'ТЕСТ "{current_test.group()}: {current_test.name()}" ' 
                                    f'Ошибка: {current_test.get_last_error()}')

                current_results.set_current_result_status(clb_tests_base.ClbTest.Status.FAIL)
                current_test.stop()
                self.next_test(a_first_test=False)

    def started(self):
        return self.__started

    def get_test_graph(self, a_group: str, a_name: str) -> List[Dict[str, Tuple[List[float], List[float]]]]:
        for idx, test in enumerate(self.tests):
            if test.group() == a_group and test.name() == a_name:
                return self.test_results[idx].get_graph_data()
        assert False, f'Тест "{a_group}: {a_name}" не найден'
