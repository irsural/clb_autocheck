from sys import float_info

from network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest


class EepromVariablesTest(ClbTest):
    def __init__(self, a_netvars: NetworkVariables, a_timeout_s: int = 30):
        super().__init__()

        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s

        self.__status = ClbTest.Status.NOT_CHECKED
        self.error_message = ""

    def prepare(self) -> bool:
        return True

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.error_message = ""

    def tick(self):
        if self.netvars.core_t_calibration.get() != 0:
            self.error_message += f"Переменная core_t_calibration = {self.netvars.core_t_calibration.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.pid_ac_voltage_k.get() != 0.06:
            self.error_message += f"Переменная pid_ac_voltage_k = {self.netvars.pid_ac_voltage_k.get()} " \
                                  f"не соответствует значению по умолчанию '0.06'\n"
        if self.netvars.pid_ac_voltage_ki.get() != 7:
            self.error_message += f"Переменная pid_ac_voltage_ki = {self.netvars.pid_ac_voltage_ki.get()} " \
                                  f"не соответствует значению по умолчанию '7'\n"
        if self.netvars.pid_ac_voltage_kd.get() != 0.5:
            self.error_message += f"Переменная pid_ac_voltage_kd = {self.netvars.pid_ac_voltage_kd.get()} " \
                                  f"не соответствует значению по умолчанию '0.5'\n"
        if self.netvars.iso_ac_voltage_k.get() != 1:
            self.error_message += f"Переменная iso_ac_voltage_k = {self.netvars.iso_ac_voltage_k.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.iso_ac_voltage_t.get() != 0:
            self.error_message += f"Переменная iso_ac_voltage_t = {self.netvars.iso_ac_voltage_t.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.acv_rate_slope.get() != 100:
            self.error_message += f"Переменная acv_rate_slope = {self.netvars.acv_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '100'\n"
        if self.netvars.pid_ac_current_k.get() != 0.06:
            self.error_message += f"Переменная pid_ac_current_k = {self.netvars.pid_ac_current_k.get()} " \
                                  f"не соответствует значению по умолчанию '0.06'\n"
        if self.netvars.pid_ac_current_ki.get() != 12:
            self.error_message += f"Переменная pid_ac_current_ki = {self.netvars.pid_ac_current_ki.get()} " \
                                  f"не соответствует значению по умолчанию '12'\n"
        if self.netvars.pid_ac_current_kd.get() != 0.5:
            self.error_message += f"Переменная pid_ac_current_kd = {self.netvars.pid_ac_current_kd.get()} " \
                                  f"не соответствует значению по умолчанию '0.5'\n"
        if self.netvars.iso_ac_current_k.get() != 1:
            self.error_message += f"Переменная iso_ac_current_k = {self.netvars.iso_ac_current_k.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.iso_ac_current_t.get() != 0:
            self.error_message += f"Переменная iso_ac_current_t = {self.netvars.iso_ac_current_t.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.aci_rate_slope.get() != 1:
            self.error_message += f"Переменная aci_rate_slope = {self.netvars.aci_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.aci_preset_voltage_rate_slope.get() != 30:
            self.error_message += f"Переменная aci_preset_voltage_rate_slope = {self.netvars.aci_preset_voltage_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '30'\n"
        if self.netvars.dead_band.get() != 0:
            self.error_message += f"Переменная dead_band = {self.netvars.dead_band.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.f_correct_off.get() != 1:
            self.error_message += f"Переменная f_correct_off = {self.netvars.f_correct_off.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.ui_correct_off.get() != 1:
            self.error_message += f"Переменная ui_correct_off = {self.netvars.ui_correct_off.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.use_eeprom_instead_of_sd_for_correct.get() != 1:
            self.error_message += f"Переменная use_eeprom_instead_of_sd_for_correct = {self.netvars.use_eeprom_instead_of_sd_for_correct.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.analog_board_temperature_max.get() != 60:
            self.error_message += f"Переменная analog_board_temperature_max = {self.netvars.analog_board_temperature_max.get()} " \
                                  f"не соответствует значению по умолчанию '60'\n"
        if self.netvars.main_board_temperature_max.get() != 70:
            self.error_message += f"Переменная main_board_temperature_max = {self.netvars.main_board_temperature_max.get()} " \
                                  f"не соответствует значению по умолчанию '70'\n"
        if self.netvars.main_board_fun_temperature_setpoint.get() != 40:
            self.error_message += f"Переменная main_board_fun_temperature_setpoint = {self.netvars.main_board_fun_temperature_setpoint.get()} " \
                                  f"не соответствует значению по умолчанию '40'\n"
        if self.netvars.main_board_fun_pid_k.get() != 0.1:
            self.error_message += f"Переменная main_board_fun_pid_k = {self.netvars.main_board_fun_pid_k.get()} " \
                                  f"не соответствует значению по умолчанию '0.1'\n"
        if self.netvars.main_board_fun_pid_ki.get() != 0.05:
            self.error_message += f"Переменная main_board_fun_pid_ki = {self.netvars.main_board_fun_pid_ki.get()} " \
                                  f"не соответствует значению по умолчанию '0.05'\n"
        if self.netvars.main_board_fun_pid_kd.get() != 0:
            self.error_message += f"Переменная main_board_fun_pid_kd = {self.netvars.main_board_fun_pid_kd.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.main_board_fun_iso_k.get() != 1:
            self.error_message += f"Переменная main_board_fun_iso_k = {self.netvars.main_board_fun_iso_k.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.main_board_fun_iso_t.get() != 0:
            self.error_message += f"Переменная main_board_fun_iso_t = {self.netvars.main_board_fun_iso_t.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.main_board_fun_rate_slope.get() != 1000:
            self.error_message += f"Переменная main_board_fun_rate_slope = {self.netvars.main_board_fun_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '1000'\n"
        if self.netvars.transistor_dc_10a_temperature_max.get() != 90:
            self.error_message += f"Переменная transistor_dc_10a_temperature_max = {self.netvars.transistor_dc_10a_temperature_max.get()} " \
                                  f"не соответствует значению по умолчанию '90'\n"
        if self.netvars.transistor_dc_10a_fun_temperature_setpoint.get() != 40:
            self.error_message += f"Переменная transistor_dc_10a_fun_temperature_setpoint = {self.netvars.transistor_dc_10a_fun_temperature_setpoint.get()} " \
                                  f"не соответствует значению по умолчанию '40'\n"
        if self.netvars.transistor_dc_10a_fun_pid_k.get() != 0.1:
            self.error_message += f"Переменная transistor_dc_10a_fun_pid_k = {self.netvars.transistor_dc_10a_fun_pid_k.get()} " \
                                  f"не соответствует значению по умолчанию '0.1'\n"
        if self.netvars.transistor_dc_10a_fun_pid_ki.get() != 0.05:
            self.error_message += f"Переменная transistor_dc_10a_fun_pid_ki = {self.netvars.transistor_dc_10a_fun_pid_ki.get()} " \
                                  f"не соответствует значению по умолчанию '0.05'\n"
        if self.netvars.transistor_dc_10a_fun_pid_kd.get() != 0:
            self.error_message += f"Переменная transistor_dc_10a_fun_pid_kd = {self.netvars.transistor_dc_10a_fun_pid_kd.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.transistor_dc_10a_fun_iso_k.get() != 1:
            self.error_message += f"Переменная transistor_dc_10a_fun_iso_k = {self.netvars.transistor_dc_10a_fun_iso_k.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.transistor_dc_10a_fun_iso_t.get() != 0:
            self.error_message += f"Переменная transistor_dc_10a_fun_iso_t = {self.netvars.transistor_dc_10a_fun_iso_t.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.transistor_dc_10a_fun_rate_slope.get() != 1000:
            self.error_message += f"Переменная transistor_dc_10a_fun_rate_slope = {self.netvars.transistor_dc_10a_fun_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '1000'\n"
        if self.netvars.peltier_1_temperature_max.get() != 60:
            self.error_message += f"Переменная peltier_1_temperature_max = {self.netvars.peltier_1_temperature_max.get()} " \
                                  f"не соответствует значению по умолчанию '60'\n"
        if self.netvars.peltier_1_temperature_setpoint.get() != 40:
            self.error_message += f"Переменная peltier_1_temperature_setpoint = {self.netvars.peltier_1_temperature_setpoint.get()} " \
                                  f"не соответствует значению по умолчанию '40'\n"
        if self.netvars.peltier_1_pid_k.get() != 0.04:
            self.error_message += f"Переменная peltier_1_pid_k = {self.netvars.peltier_1_pid_k.get()} " \
                                  f"не соответствует значению по умолчанию '0.04:'\n"
        if self.netvars.peltier_1_pid_ki.get() != 0.1:
            self.error_message += f"Переменная peltier_1_pid_ki = {self.netvars.peltier_1_pid_ki.get()} " \
                                  f"не соответствует значению по умолчанию '0.1'\n"
        if self.netvars.peltier_1_pid_kd.get() != 0:
            self.error_message += f"Переменная peltier_1_pid_kd = {self.netvars.peltier_1_pid_kd.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.peltier_1_iso_k.get() != 1:
            self.error_message += f"Переменная peltier_1_iso_k = {self.netvars.peltier_1_iso_k.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.peltier_1_iso_t.get() != 0:
            self.error_message += f"Переменная peltier_1_iso_t = {self.netvars.peltier_1_iso_t.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.peltier_1_rate_slope.get() != 0.4:
            self.error_message += f"Переменная peltier_1_rate_slope = {self.netvars.peltier_1_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '0.4'\n"
        if self.netvars.peltier_2_temperature_max.get() != 60:
            self.error_message += f"Переменная peltier_2_temperature_max = {self.netvars.peltier_2_temperature_max.get()} " \
                                  f"не соответствует значению по умолчанию '60'\n"
        if self.netvars.peltier_2_temperature_setpoint.get() != 40:
            self.error_message += f"Переменная peltier_2_temperature_setpoint = {self.netvars.peltier_2_temperature_setpoint.get()} " \
                                  f"не соответствует значению по умолчанию '40'\n"
        if self.netvars.peltier_2_pid_k.get() != 0.1:
            self.error_message += f"Переменная peltier_2_pid_k = {self.netvars.peltier_2_pid_k.get()} " \
                                  f"не соответствует значению по умолчанию '0.1'\n"
        if self.netvars.peltier_2_pid_ki.get() != 0.1:
            self.error_message += f"Переменная peltier_2_pid_ki = {self.netvars.peltier_2_pid_ki.get()} " \
                                  f"не соответствует значению по умолчанию '0.1'\n"
        if self.netvars.peltier_2_pid_kd.get() != 0:
            self.error_message += f"Переменная peltier_2_pid_kd = {self.netvars.peltier_2_pid_kd.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.peltier_2_iso_k.get() != 1:
            self.error_message += f"Переменная peltier_2_iso_k = {self.netvars.peltier_2_iso_k.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.peltier_2_iso_t.get() != 0:
            self.error_message += f"Переменная peltier_2_iso_t = {self.netvars.peltier_2_iso_t.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.peltier_2_rate_slope.get() != 0.4:
            self.error_message += f"Переменная peltier_2_rate_slope = {self.netvars.peltier_2_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '0.4'\n"
        if self.netvars.peltier_3_temperature_max.get() != 60:
            self.error_message += f"Переменная peltier_3_temperature_max = {self.netvars.peltier_3_temperature_max.get()} " \
                                  f"не соответствует значению по умолчанию '60'\n"
        if self.netvars.peltier_3_temperature_setpoint.get() != 40:
            self.error_message += f"Переменная peltier_3_temperature_setpoint = {self.netvars.peltier_3_temperature_setpoint.get()} " \
                                  f"не соответствует значению по умолчанию '40'\n"
        if self.netvars.peltier_3_pid_k.get() != 0.1:
            self.error_message += f"Переменная peltier_3_pid_k = {self.netvars.peltier_3_pid_k.get()} " \
                                  f"не соответствует значению по умолчанию '0.1'\n"
        if self.netvars.peltier_3_pid_ki.get() != 0.1:
            self.error_message += f"Переменная peltier_3_pid_ki = {self.netvars.peltier_3_pid_ki.get()} " \
                                  f"не соответствует значению по умолчанию '0.1'\n"
        if self.netvars.peltier_3_pid_kd.get() != 0:
            self.error_message += f"Переменная peltier_3_pid_kd = {self.netvars.peltier_3_pid_kd.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.peltier_3_iso_k.get() != 1:
            self.error_message += f"Переменная peltier_3_iso_k = {self.netvars.peltier_3_iso_k.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.peltier_3_iso_t.get() != 0:
            self.error_message += f"Переменная peltier_3_iso_t = {self.netvars.peltier_3_iso_t.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.peltier_3_rate_slope.get() != 0.4:
            self.error_message += f"Переменная peltier_3_rate_slope = {self.netvars.peltier_3_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '0.4'\n"
        if self.netvars.peltier_4_temperature_max.get() != 70:
            self.error_message += f"Переменная peltier_4_temperature_max = {self.netvars.peltier_4_temperature_max.get()} " \
                                  f"не соответствует значению по умолчанию '70'\n"
        if round(self.netvars.volume.get(), 9) != 0.01:
            self.error_message += f"Переменная volume = {round(self.netvars.volume.get(), 9)} " \
                                  f"не соответствует значению по умолчанию '0.01'\n"
        if self.netvars.result_id.get() != 0:
            self.error_message += f"Переменная result_id = {self.netvars.result_id.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.f_calibr_coeff.get() != 0.999886999072:
            self.error_message += f"Переменная f_calibr_coeff = {self.netvars.f_calibr_coeff.get()} " \
                                  f"не соответствует значению по умолчанию '0.999886999072'\n"
        if abs(self.netvars.time_calibr_coeff.get() - 0.999913223168079) > float_info.epsilon:
            self.error_message += f"Переменная time_calibr_coeff = {self.netvars.time_calibr_coeff.get()} " \
                                  f"не соответствует значению по умолчанию '0.999913223168079'\n"
        if self.netvars.id.get() == 0:
            self.error_message += f"Переменная id = {self.netvars.id.get()} " \
                                  f"не установлена\n"
        if self.netvars.peltier_4_temperature_setpoint.get() != 40:
            self.error_message += f"Переменная peltier_4_temperature_setpoint = {self.netvars.peltier_4_temperature_setpoint.get()} " \
                                  f"не соответствует значению по умолчанию '40'\n"
        if self.netvars.peltier_4_pid_k.get() != 0.2:
            self.error_message += f"Переменная peltier_4_pid_k = {self.netvars.peltier_4_pid_k.get()} " \
                                  f"не соответствует значению по умолчанию '0.2'\n"
        if self.netvars.peltier_4_pid_ki.get() != 0.015:
            self.error_message += f"Переменная peltier_4_pid_ki = {self.netvars.peltier_4_pid_ki.get()} " \
                                  f"не соответствует значению по умолчанию '0.015'\n"
        if self.netvars.peltier_4_pid_kd.get() != 0:
            self.error_message += f"Переменная peltier_4_pid_kd = {self.netvars.peltier_4_pid_kd.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.peltier_4_iso_k.get() != 1:
            self.error_message += f"Переменная peltier_4_iso_k = {self.netvars.peltier_4_iso_k.get()} " \
                                  f"не соответствует значению по умолчанию '1'\n"
        if self.netvars.peltier_4_iso_t.get() != 0:
            self.error_message += f"Переменная peltier_4_iso_t = {self.netvars.peltier_4_iso_t.get()} " \
                                  f"не соответствует значению по умолчанию '0'\n"
        if self.netvars.peltier_4_rate_slope.get() != 0.4:
            self.error_message += f"Переменная peltier_4_rate_slope = {self.netvars.peltier_4_rate_slope.get()} " \
                                  f"не соответствует значению по умолчанию '0.4'\n"
        # if self.netvars.fun_max_level_reset_mark.get() != 0:
        #     self.error_message += f"Переменная fun_max_level_reset_mark = {self.netvars.fun_max_level_reset_mark.get()} " \
        #                           f"не соответствует значению по умолчанию '0'\n"

        if not self.error_message:
            self.__status = ClbTest.Status.SUCCESS
        else:
            self.__status = ClbTest.Status.FAIL

    def status(self) -> ClbTest.Status:
        return self.__status

    def timeout(self) -> float:
        return self.__timeout_s

    def has_error(self) -> bool:
        return bool(self.error_message)

    def get_last_error(self) -> str:
        return self.error_message
