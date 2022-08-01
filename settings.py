from irspy.qt.qt_settings_ini_parser import QtSettings


def get_clb_autocheck_settings():
    settings = QtSettings("./clb_autocheck.ini", [
        QtSettings.VariableInfo(a_name="fixed_step_list", a_section="PARAMETERS", a_type=QtSettings.ValueType.LIST_FLOAT, a_default=[0.0001,0.01,0.1,1,10,20,100]),
        QtSettings.VariableInfo(a_name="checkbox_states", a_section="PARAMETERS", a_type=QtSettings.ValueType.LIST_INT),
        QtSettings.VariableInfo(a_name="fixed_step_idx", a_section="PARAMETERS", a_type=QtSettings.ValueType.INT),
        QtSettings.VariableInfo(a_name="rough_step", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=0.5),
        QtSettings.VariableInfo(a_name="common_step", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=0.05),
        QtSettings.VariableInfo(a_name="exact_step", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=0.002),
        QtSettings.VariableInfo(a_name="tstlan_update_time", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=0.2),
        QtSettings.VariableInfo(a_name="tstlan_show_marks", a_section="PARAMETERS", a_type=QtSettings.ValueType.INT, a_default=0),
        QtSettings.VariableInfo(a_name="tstlan_marks", a_section="PARAMETERS", a_type=QtSettings.ValueType.LIST_INT),
        QtSettings.VariableInfo(a_name="tstlan_graphs", a_section="PARAMETERS", a_type=QtSettings.ValueType.LIST_INT),
        QtSettings.VariableInfo(a_name="tests_repeat_count", a_section="PARAMETERS", a_type=QtSettings.ValueType.LIST_INT),
        QtSettings.VariableInfo(a_name="tests_collapsed_states", a_section="PARAMETERS", a_type=QtSettings.ValueType.LIST_INT),
        QtSettings.VariableInfo(a_name="last_save_results_folder", a_section="PARAMETERS", a_type=QtSettings.ValueType.STRING),
        QtSettings.VariableInfo(a_name="aux_correction_deviation", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=10),
        QtSettings.VariableInfo(a_name="aux_deviation", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=2),
        QtSettings.VariableInfo(a_name="aux_voltage_25_discretes_60v", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=18),
        QtSettings.VariableInfo(a_name="aux_voltage_230_discretes_60v", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=61.2),
        QtSettings.VariableInfo(a_name="aux_voltage_25_discretes_200v", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=61),
        QtSettings.VariableInfo(a_name="aux_voltage_230_discretes_200v", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=215),
        QtSettings.VariableInfo(a_name="aux_voltage_25_discretes_600v", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=165),
        QtSettings.VariableInfo(a_name="aux_voltage_230_discretes_600v", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=605),
        QtSettings.VariableInfo(a_name="aux_voltage_25_discretes_4v", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=1.73),
        QtSettings.VariableInfo(a_name="aux_voltage_230_discretes_4v", a_section="PARAMETERS", a_type=QtSettings.ValueType.FLOAT, a_default=4.6),
    ])
    return settings
