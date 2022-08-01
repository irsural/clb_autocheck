from typing import List, Dict, Tuple, Union
import logging
import time
import json

from PyQt5 import QtCore

from irspy.clb.network_variables import BufferedVariable
from clb_tests import tests_base
from irspy import utils


class TestResults:
    def __init__(self):
        self.statuses = []
        self.errors = []
        self.variables_to_graph = {}
        self.graph_data = []
        self.graph_normalize_time_value = 0

    def set_current_result(self, a_status: tests_base.ClbTest.Status, a_error: str):
        self.statuses[-1] = a_status
        self.errors[-1] = a_error

    def new_result(self):
        self.statuses.append(tests_base.ClbTest.Status.NOT_CHECKED)
        self.errors.append("")
        if self.variables_to_graph:
            self.graph_data.append({name: ([], []) for name in self.variables_to_graph.keys()})

    def delete_results(self):
        self.statuses = []
        self.errors = []
        self.variables_to_graph = {}
        self.graph_data = []

    def get_final_status(self) -> tests_base.ClbTest.Status:
        if not self.statuses or self.statuses[0] == tests_base.ClbTest.Status.NOT_CHECKED:
            return tests_base.ClbTest.Status.NOT_CHECKED
        else:
            for status in self.statuses:
                assert status != (tests_base.ClbTest.Status.IN_PROCESS, tests_base.ClbTest.Status.NOT_CHECKED)
                if status == tests_base.ClbTest.Status.FAIL:
                    return tests_base.ClbTest.Status.FAIL
            return tests_base.ClbTest.Status.SUCCESS

    def get_errors(self):
        return self.errors

    def get_results_count(self) -> int:
        return len(self.statuses)

    def get_success_results_count(self) -> int:
        return self.statuses.count(tests_base.ClbTest.Status.SUCCESS)

    def get_graph_data(self) -> List[Dict[str, Tuple[List[float], List[float]]]]:
        return self.graph_data

    def set_variables_to_graph(self, a_variables_to_graph: Dict[str, BufferedVariable]):
        self.variables_to_graph = a_variables_to_graph

    def read_variables_to_graph(self):
        timestamp = time.time()

        for variable in self.variables_to_graph.keys():
            value = self.variables_to_graph[variable].get()
            current_graph = self.graph_data[-1][variable]

            if not current_graph[0]:
                self.graph_normalize_time_value = timestamp
            # Список X-ов
            current_graph[0].append(round(timestamp - self.graph_normalize_time_value, 3))
            # Список Y-ов
            current_graph[1].append(value)

    def data_to_serialize(self):
        results_dict = self.__dict__
        # Не сериализуется нормально, сохранять не обязательно
        results_dict["variables_to_graph"] = {}
        return results_dict
        # return json.dumps(self, cls=TestResultsEncoder, indent=4)

    def __str__(self):
        return f"{self.statuses}\n{self.graph_data}"


class TestResultsEncoder(json.JSONEncoder):
    def default(self, o):
        results_dict = o.__dict__
        # Не сериализуется нормально, сохранять не обязательно
        results_dict["variables_to_graph"] = {}
        return results_dict


class TestsConductor(QtCore.QObject):
    test_status_changed = QtCore.pyqtSignal(str, str, tests_base.ClbTest.Status, int)
    graphs_have_been_updated = QtCore.pyqtSignal()
    tests_done = QtCore.pyqtSignal()

    def __init__(self, a_tests: List[tests_base.ClbTest]):
        super().__init__()

        self.tests = a_tests
        self.test_results = [TestResults() for _ in range(len(self.tests))]

        self.enabled_tests = []
        self.prepare_timer = utils.Timer(1.5)
        self.timeout_timer = utils.Timer(30)

        # Работает в цикличном режиме
        self.read_graphs_time = utils.Timer(0.1)
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
                                              tests_base.ClbTest.Status.IN_PROCESS,
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
                if current_test.status() == tests_base.ClbTest.Status.NOT_CHECKED:
                    if self.prepare_timer.check():
                        if current_test.prepare():
                            logging.info(f"Успешная подготовка")
                            current_test.start()
                        else:
                            self.prepare_timer.start()

                elif current_test.status() == tests_base.ClbTest.Status.IN_PROCESS:
                    current_test.tick()

                    if self.read_graphs_time.check():
                        self.read_graphs_time.start()
                        current_results.read_variables_to_graph()
                        self.graphs_have_been_updated.emit()

                elif current_test.status() in (tests_base.ClbTest.Status.SUCCESS, tests_base.ClbTest.Status.FAIL):
                    logging.info(f'ТЕСТ "{current_test.group()}: {current_test.name()}" '
                                 f'результат {current_test.status().name}')

                    current_test_status = current_test.status()
                    error = "" if not current_test.has_error() else current_test.get_last_error()
                    current_results.set_current_result(current_test_status, error)
                    current_test.stop()

                    if current_test_status == tests_base.ClbTest.Status.FAIL and current_test.abort_on_fail():
                        logging.warning("Провал данного теста критичен. Следующие тесты проводиться не будут")
                        self.stop()
                        self.tests_done.emit()
                    else:
                        self.next_test(a_first_test=False)
            else:
                logging.debug(f'ТЕСТ "{current_test.group()}: {current_test.name()}" TIMEOUT')

                error = "" if not current_test.has_error() else current_test.get_last_error()
                current_results.set_current_result(tests_base.ClbTest.Status.FAIL, f"{error} ТАЙМАУТ\n")
                current_test.stop()
                if current_test.abort_on_fail():
                    logging.warning("Провал данного теста критичен. Следующие тесты проводиться не будут")
                    self.stop()
                    self.tests_done.emit()
                else:
                    self.next_test(a_first_test=False)

    def started(self):
        return self.__started

    def get_test_graph(self, a_group: str, a_name: str) -> List[Dict[str, Tuple[List[float], List[float]]]]:
        for idx, test in enumerate(self.tests):
            if test.group() == a_group and test.name() == a_name:
                return self.test_results[idx].get_graph_data()
        assert False, f'Тест "{a_group}: {a_name}" не найден'

    def get_test_errors(self, a_group: str, a_name: str) -> List[str]:
        for idx, test in enumerate(self.tests):
            if test.group() == a_group and test.name() == a_name:
                return self.test_results[idx].get_errors()
        assert False, f'Тест "{a_group}: {a_name}" не найден'

    def get_test_results(self, a_group: str, a_name: str) -> Union[None, TestResults]:
        for idx, test in enumerate(self.tests):
            if test.group() == a_group and test.name() == a_name:
                return self.test_results[idx]
        return None

    def set_test_results(self, a_group: str, a_name: str, a_test_results: Dict):
        for idx, test in enumerate(self.tests):
            if test.group() == a_group and test.name() == a_name:
                test_result = TestResults()
                test_result.statuses = a_test_results["statuses"]
                test_result.errors = a_test_results["errors"]
                test_result.variables_to_graph = {}
                test_result.graph_data = a_test_results["graph_data"]
                test_result.graph_normalize_time_value = a_test_results["graph_normalize_time_value"]

                self.test_results[idx] = test_result

                self.test_status_changed.emit(a_group, a_name, test_result.get_final_status(),
                                              test_result.get_success_results_count())
                return
        raise ValueError
