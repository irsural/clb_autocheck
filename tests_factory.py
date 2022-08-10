from network_variables_database import NetvarsDatabase
from irspy.clb.network_variables import NetworkVariables
import irspy.clb.calibrator_constants as clb
from irspy.qt.qt_settings_ini_parser import QtSettings
from irspy.clb.clb_dll import ClbDrv

from clb_tests.test_eeprom_variables import EepromVariablesTest
from clb_tests.test_supply_voltage import SupplyVoltageTest
from clb_tests.test_release_check import ReleaseCheckTest
from clb_tests.test_peltier import PeltierTest
from clb_tests.test_coolers import CoolerTest
from clb_tests.test_signals import SignalTest
from clb_tests.test_cables import CablesTest
from clb_tests.test_aux_stabilizers import AuxStabilizersTest
# from clb_tests.tests_base import EmptyTest


def create_cooler_tests(a_cooler: CoolerTest.CoolerLocation, a_netvars: NetworkVariables):

    test = CoolerTest(a_cooler_location=a_cooler, a_netvars=a_netvars)
    test.set_group("Кулеры")
    test.set_name(CoolerTest.COOLER_LOCATION_TO_TEXT[a_cooler])
    test.set_variables_to_graph({"Выход pid-регулятора": a_netvars.main_board_fun_pid_out,
                                 "Скорость (об/мин)": a_netvars.main_board_fun_speed})
    return test


def create_peltier_tests(a_peltier: PeltierTest.PeltierNumber, a_netvars: NetworkVariables,
                         a_timeout=160):
    test = PeltierTest(a_peltier_number=a_peltier, a_netvars=a_netvars, a_ready_hold_timer=30,
                       a_wait_peltier_timeout_s=a_timeout, a_timeout_s=a_timeout * 3)
    test.set_group("Пельтье")
    test.set_name(f"№{int(a_peltier)}")

    graph_variables_templates = {"Уставка": "peltier_{}_temperature_setpoint",
                                 "Температура": "peltier_{}_temperature",
                                 "Выход pid-регулятора": "peltier_{}_pid_out",
                                 "Бит готовности": "peltier_{}_ready"}

    graph_variables = {}
    for name, template in graph_variables_templates.items():
        graph_variables[name] = getattr(a_netvars, template.format(int(a_peltier)))

    test.set_variables_to_graph(graph_variables)

    return test


def create_tests(a_calibrator: ClbDrv, a_netvars: NetworkVariables, a_netvars_db: NetvarsDatabase,
                 a_settings: QtSettings):
    tests = []
    # -----------------------------------------------------------------------------------------------------
    test = CablesTest(a_netvars=a_netvars)
    test.set_group("Тесты")
    test.set_name("Шлейфы")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = SupplyVoltageTest(a_netvars=a_netvars, a_success_timeout_s=30, a_timeout_s=60)
    test.set_group("Тесты")
    test.set_name("Напряжения питания")
    test.set_variables_to_graph({
        "Внутр. стабилизатор 12 В": a_netvars.inner_stabilizer_12v_voltage,
        "Внутр. стабилизатор 9 В": a_netvars.inner_stabilizer_9v_voltage,
        "Внутр. стабилизатор 5 В": a_netvars.inner_stabilizer_5v_voltage,
        "Внутр. стабилизатор +2.5 В": a_netvars.inner_stabilizer_2_5v_pos_voltage,
        "Внутр. стабилизатор -2.5 В": a_netvars.inner_stabilizer_2_5v_neg_voltage,
        "Питание кулеров": a_netvars.cooling_power_supply_voltage})
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = EepromVariablesTest(a_netvars_db=a_netvars_db, a_calibrator=a_calibrator)
    test.set_group("Тесты")
    test.set_name("Сетевые переменные")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = ReleaseCheckTest(a_netvars=a_netvars)
    test.set_group("Тесты")
    test.set_name("Проверка перед отправкой")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    tests.append(create_cooler_tests(CoolerTest.CoolerLocation.MAIN_BOARD, a_netvars))
    tests.append(create_cooler_tests(CoolerTest.CoolerLocation.TRANSISTOR_DC, a_netvars))
    # -----------------------------------------------------------------------------------------------------
    tests.append(create_peltier_tests(PeltierTest.PeltierNumber.FIRST, a_netvars))
    tests.append(create_peltier_tests(PeltierTest.PeltierNumber.SECOND, a_netvars))
    tests.append(create_peltier_tests(PeltierTest.PeltierNumber.THIRD, a_netvars))
    tests.append(create_peltier_tests(PeltierTest.PeltierNumber.FOURTH, a_netvars, 200))
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
    test.set_name("630 В")
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
    test = SignalTest(a_amplitude=0.1, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars, a_calibrator=a_calibrator,
                      a_timeout_s=60)
    test.set_group("I~")
    test.set_name("110 мА")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=1, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars, a_calibrator=a_calibrator,
                      a_timeout_s=60)
    test.set_group("I~")
    test.set_name("1.1 А")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    test = SignalTest(a_amplitude=10, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars, a_calibrator=a_calibrator,
                      a_timeout_s=60)
    test.set_group("I~")
    test.set_name("11 А")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow,
                                 "Стабилизатор 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage})
    tests.append(test)

    # ТЕСТЫ ПРЕДВАРИТЕЛЬНЫХ СТАБИЛИЗАТОРОВ ДОЛЖНЫ БЫТЬ ПОСЛЕДНИМИ ------------------------------------------------------

    ref_v_map = {AuxStabilizersTest.AuxType.V60: (12, 50, 88, 126, 164, 202, 240)}
    test = AuxStabilizersTest(a_settings=a_settings, a_ref_v_map=ref_v_map, a_netvars=a_netvars,
                              a_aux_fail_timeout_s=10, a_hold_voltage_timeout_s=2, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("60 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: (107,),
                 AuxStabilizersTest.AuxType.V200: (12, 50, 88, 126, 164, 202, 240)}
    test = AuxStabilizersTest(a_settings=a_settings, a_ref_v_map=ref_v_map, a_netvars=a_netvars,
                              a_aux_fail_timeout_s=10, a_hold_voltage_timeout_s=2, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("200 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 600 В": a_netvars.aux_stabilizer_adc_dc_600v_voltage,
                                 "Уставка на 600 В": a_netvars.aux_stabilizer_600v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: (107,),
                 AuxStabilizersTest.AuxType.V600: (12, 50, 88, 126, 164, 202, 240)}
    test = AuxStabilizersTest(a_settings=a_settings, a_ref_v_map=ref_v_map, a_netvars=a_netvars,
                              a_aux_fail_timeout_s=10, a_hold_voltage_timeout_s=2, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("600 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 600 В": a_netvars.aux_stabilizer_adc_dc_600v_voltage,
                                 "Уставка на 600 В": a_netvars.aux_stabilizer_600v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: (51,),
                 AuxStabilizersTest.AuxType.V4: (12, 50, 88, 126, 164, 202, 240)}
    test = AuxStabilizersTest(a_settings=a_settings, a_ref_v_map=ref_v_map, a_netvars=a_netvars,
                              a_aux_fail_timeout_s=10, a_hold_voltage_timeout_s=2, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("4 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage,
                                 "Уставка на 4 В": a_netvars.aux_stabilizer_4v_dac_code_float})
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    return tests
