from network_variables_database import NetvarsDatabase
from network_variables import NetworkVariables
import calibrator_constants as clb
from clb_dll import ClbDrv

from clb_tests.test_eeprom_variables import EepromVariablesTest
from clb_tests.test_supply_voltage import SupplyVoltageTest
from clb_tests.test_release_check import ReleaseCheckTest
from clb_tests.test_peltier import PeltierTest
from clb_tests.test_coolers import CoolerTest
from clb_tests.test_signals import SignalTest
from clb_tests.test_cables import CablesTest
from clb_tests.test_aux_stabilizers import AuxStabilizersTest, Aux60vControl, Aux600vControl, Aux4vControl
# from clb_tests.tests_base import EmptyTest


def create_tests(a_calibrator: ClbDrv, a_netvars: NetworkVariables, a_netvars_db: NetvarsDatabase):
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
    test.set_variables_to_graph({"Внутр. стабилизатор 12 В": a_netvars.inner_stabilizer_12v_voltage,
                                 "Внутр. стабилизатор 9 В": a_netvars.inner_stabilizer_9v_voltage,
                                 "Внутр. стабилизатор 5 В": a_netvars.inner_stabilizer_5v_voltage,
                                 "Внутр. стабилизатор +2.5 В": a_netvars.inner_stabilizer_2_5v_pos_voltage,
                                 "Внутр. стабилизатор -2.5 В": a_netvars.inner_stabilizer_2_5v_neg_voltage,
                                 "Питание кулеров": a_netvars.cooling_power_supply_voltage})
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    ref_v_map = {AuxStabilizersTest.AuxType.V60: 14.746}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 60v: 20 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: 40.}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 60v: 40 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: 60.}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 60v: 60 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: 14.746, AuxStabilizersTest.AuxType.V600: 13.3}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 600v: 20 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 600 В": a_netvars.aux_stabilizer_adc_dc_600v_voltage,
                                 "Уставка на 600 В": a_netvars.aux_stabilizer_600v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: 20., AuxStabilizersTest.AuxType.V600: 200}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 600v: 200 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 600 В": a_netvars.aux_stabilizer_adc_dc_600v_voltage,
                                 "Уставка на 600 В": a_netvars.aux_stabilizer_600v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: 20., AuxStabilizersTest.AuxType.V600: 600}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 600v: 600 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 600 В": a_netvars.aux_stabilizer_adc_dc_600v_voltage,
                                 "Уставка на 600 В": a_netvars.aux_stabilizer_600v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: 14.746, AuxStabilizersTest.AuxType.V4: 2}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 4v: 2 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage,
                                 "Уставка на 4 В": a_netvars.aux_stabilizer_4v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: 20., AuxStabilizersTest.AuxType.V4: 3}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 4v: 3 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage,
                                 "Уставка на 4 В": a_netvars.aux_stabilizer_4v_dac_code_float})
    tests.append(test)

    ref_v_map = {AuxStabilizersTest.AuxType.V60: 20., AuxStabilizersTest.AuxType.V4: 4}
    test = AuxStabilizersTest(a_ref_v_map=ref_v_map, a_netvars=a_netvars, a_aux_fail_timeout_s=40,
                              a_hold_voltage_timeout_s=10, a_timeout_s=100)
    test.set_group("Предварительные стабилизаторы")
    test.set_name("AUX 4v: 4 В")
    test.set_variables_to_graph({"Напряжение на 60 В": a_netvars.aux_stabilizer_adc_dc_40v_voltage,
                                 "Уставка на 60 В": a_netvars.aux_stabilizer_45v_dac_code_float,
                                 "Напряжение на 4 В": a_netvars.aux_stabilizer_adc_dc_4v_voltage,
                                 "Уставка на 4 В": a_netvars.aux_stabilizer_4v_dac_code_float})
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
    test = PeltierTest(a_peltier_number=PeltierTest.PeltierNumber.FIRST, a_netvars=a_netvars, a_ready_hold_timer=30,
                       a_wait_peltier_timeout_s=160, a_timeout_s=400)
    test.set_group("Пельтье")
    test.set_name("№1")
    test.set_variables_to_graph({"Уставка": a_netvars.peltier_1_temperature_setpoint,
                                 "Температура": a_netvars.peltier_1_temperature,
                                 "Выход pid-регулятора": a_netvars.peltier_1_pid_out,
                                 "amplitude_code_float": a_netvars.peltier_1_amplitude_code_float,
                                 "Бит готовности": a_netvars.peltier_1_ready})
    tests.append(test)

    test = PeltierTest(a_peltier_number=PeltierTest.PeltierNumber.SECOND, a_netvars=a_netvars, a_ready_hold_timer=30,
                       a_wait_peltier_timeout_s=160, a_timeout_s=400)
    test.set_group("Пельтье")
    test.set_name("№2")
    test.set_variables_to_graph({"Уставка": a_netvars.peltier_2_temperature_setpoint,
                                 "Температура": a_netvars.peltier_2_temperature,
                                 "Выход pid-регулятора": a_netvars.peltier_2_pid_out,
                                 "Бит готовности": a_netvars.peltier_2_ready})
    tests.append(test)

    test = PeltierTest(a_peltier_number=PeltierTest.PeltierNumber.THIRD, a_netvars=a_netvars, a_ready_hold_timer=30,
                       a_wait_peltier_timeout_s=160, a_timeout_s=400)
    test.set_group("Пельтье")
    test.set_name("№3")
    test.set_variables_to_graph({"Уставка": a_netvars.peltier_3_temperature_setpoint,
                                 "Температура": a_netvars.peltier_3_temperature,
                                 "Выход pid-регулятора": a_netvars.peltier_3_pid_out,
                                 "Бит готовности": a_netvars.peltier_3_ready})
    tests.append(test)

    test = PeltierTest(a_peltier_number=PeltierTest.PeltierNumber.FOURTH, a_netvars=a_netvars, a_ready_hold_timer=30,
                       a_wait_peltier_timeout_s=160, a_timeout_s=400)
    test.set_group("Пельтье")
    test.set_name("№4")
    test.set_variables_to_graph({"Уставка": a_netvars.peltier_4_temperature_setpoint,
                                 "Температура": a_netvars.peltier_4_temperature,
                                 "Выход pid-регулятора": a_netvars.peltier_4_pid_out,
                                 "Бит готовности": a_netvars.peltier_4_ready})
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
    # -----------------------------------------------------------------------------------------------------
    return tests
