import clb_tests
import calibrator_constants as clb
from network_variables import NetworkVariables, BufferedVariable
from clb_dll import ClbDrv


def create_tests(a_calibrator: ClbDrv, a_netvars: NetworkVariables):
    tests = []
    # -----------------------------------------------------------------------------------------------------
    test = clb_tests.EmptyTest()
    test.set_group("Шлейфы")
    test.set_name("Передний")
    tests.append(test)

    test = clb_tests.EmptyTest()
    test.set_group("Шлейфы")
    test.set_name("Задний")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = clb_tests.EmptyTest()
    test.set_group("Кулеры")
    test.set_name("Основная плата")
    tests.append(test)

    test = clb_tests.EmptyTest()
    test.set_group("Кулеры")
    test.set_name("Транзистор DC")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = clb_tests.EmptyTest()
    test.set_group("Пельтье")
    test.set_name("№1")
    tests.append(test)

    test = clb_tests.EmptyTest()
    test.set_group("Пельтье")
    test.set_name("№2")
    tests.append(test)

    test = clb_tests.EmptyTest()
    test.set_group("Пельтье")
    test.set_name("№3")
    tests.append(test)

    test = clb_tests.EmptyTest()
    test.set_group("Пельтье")
    test.set_name("№4")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = clb_tests.EmptyTest()
    test.set_group("Другое")
    test.set_name("SD карта")
    tests.append(test)

    test = clb_tests.EmptyTest()
    test.set_group("Другое")
    test.set_name("Сетевые переменные")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = clb_tests.SignalTest(a_amplitude=0.04, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("40 мВ")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow})
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=0.21, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("420 мВ")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=4, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("4 В")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=43, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("43 В")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=200, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("200 В")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=400, a_signal_type=clb.SignalType.DCV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U=")
    test.set_name("635 В")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = clb_tests.SignalTest(a_amplitude=0.1, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("110 мВ")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=1, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("1.1 В")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=10, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("11 В")
    test.set_variables_to_graph({"Напряжение на выходе": a_netvars.fast_adc_slow})
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=100, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("110 В")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=400, a_signal_type=clb.SignalType.ACV, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("U~")
    test.set_name("600 В")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = clb_tests.SignalTest(a_amplitude=0.0001, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("110 мкА")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=0.001, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("1.1 мА")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=0.01, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("11 мА")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=0.1, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("110 мА")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=1, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("1.1 А")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=10, a_signal_type=clb.SignalType.DCI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I=")
    test.set_name("11 А")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    test = clb_tests.SignalTest(a_amplitude=0.1, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I~")
    test.set_name("110 мА")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=1, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I~")
    test.set_name("1.1 А")
    tests.append(test)

    test = clb_tests.SignalTest(a_amplitude=10, a_signal_type=clb.SignalType.ACI, a_netvars=a_netvars,
                                a_calibrator=a_calibrator)
    test.set_group("I~")
    test.set_name("11 А")
    tests.append(test)
    # -----------------------------------------------------------------------------------------------------
    return tests
