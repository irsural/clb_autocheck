from network_variables_database import NetvarsDatabase
from network_variables import NetworkVariables
import calibrator_constants as clb
from clb_dll import ClbDrv

from clb_tests.test_eeprom_variables import EepromVariablesTest
from clb_tests.test_release_check import ReleaseCheckTest
from clb_tests.test_coolers import CoolerTest
from clb_tests.test_signals import SignalTest
from clb_tests.test_cables import CablesTest
from clb_tests.tests_base import EmptyTest


def create_tests(a_calibrator: ClbDrv, a_netvars: NetworkVariables, a_netvars_db: NetvarsDatabase):
    tests = []
    # -----------------------------------------------------------------------------------------------------
    test = CablesTest(a_netvars=a_netvars)
    test.set_group("Тесты")
    test.set_name("Шлейфы")
    tests.append(test)

    test = EepromVariablesTest(a_netvars_db=a_netvars_db, a_calibrator=a_calibrator)
    test.set_group("Тесты")
    test.set_name("Сетевые переменные")
    tests.append(test)

    test = ReleaseCheckTest(a_netvars=a_netvars)
    test.set_group("Тесты")
    test.set_name("Проверка перед отправкой")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = CoolerTest(a_cooler_location=CoolerTest.CoolerLocation.MAIN_BOARD, a_netvars=a_netvars)
    test.set_group("Кулеры")
    test.set_name("Основная плата")
    test.set_variables_to_graph({"Выход pid-регулятора": a_netvars.main_board_fun_pid_out,
                                 "Скорость (об/мин)": a_netvars.main_board_fun_speed})
    tests.append(test)

    test = CoolerTest(a_cooler_location=CoolerTest.CoolerLocation.TRANSISTOR_DC,
                      a_netvars=a_netvars)
    test.set_group("Кулеры")
    test.set_name("Транзистор DC")
    test.set_variables_to_graph({"Выход pid-регулятора": a_netvars.transistor_dc_10a_fun_pid_out,
                                 "Скорость (об/мин)": a_netvars.transistor_dc_10a_fun_speed})
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = EmptyTest()
    test.set_group("Пельтье")
    test.set_name("№1")
    tests.append(test)

    test = EmptyTest()
    test.set_group("Пельтье")
    test.set_name("№2")
    tests.append(test)

    test = EmptyTest()
    test.set_group("Пельтье")
    test.set_name("№3")
    tests.append(test)

    test = EmptyTest()
    test.set_group("Пельтье")
    test.set_name("№4")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = SignalTest(a_amplitude=0.04, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars,
                      a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("40 мВ")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=0.21, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars,
                      a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("420 мВ")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=4, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("4 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=43, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("43 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=200, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("200 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Стабилизатор 600 В": a_netvars.aux_stabilizer_adc_dc_600v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=400, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("635 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Стабилизатор 600 В": a_netvars.aux_stabilizer_adc_dc_600v_voltage})
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = SignalTest(a_amplitude=0.1, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("110 мВ")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=1, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("1.1 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=10, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("11 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=100, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars,
                      a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("110 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=400, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("600 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = SignalTest(a_amplitude=0.0001, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                      a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("110 мкА")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Стабилизатор 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=0.001, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                      a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("1.1 мА")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Стабилизатор 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=0.01, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                      a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("11 мА")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Стабилизатор 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=0.1, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("110 мА")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Стабилизатор 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=1, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("1.1 А")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Стабилизатор 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=10, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("11 А")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Стабилизатор 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage})
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = SignalTest(a_amplitude=0.1, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("I~")
    test.set_name("110 мА")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=1, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("I~")
    test.set_name("1.1 А")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=10, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars, a_calibrator=a_calibrator)
    test.set_group("I~")
    test.set_name("11 А")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    return tests
