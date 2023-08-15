from rcdb.model import ConditionType

class SBSConditions(object):
    """
    Default conditions are defined in rcdb
    Below are additional conditions for SBS database
    """

    BEAM_ENERGY = "beam_energy"
    BEAM_CURRENT = "beam_current"
    TARGET = "target"
    BB_ANGLE = "bb_angle"
    SBS_ANGLE = "sbs_angle"
    SBS_CURRENT = "sbs_current"
    BB_CURRENT = "bb_current"

def create_condition_types(db):
    
    all_types_dict = {t.name: t for t in db.get_condition_types()}
    
    def create_condition_type(name, value_type, description=""):
        all_types_dict[name] if name in all_types_dict.keys() \
            else db.create_condition_type(name, value_type, description)
    
    # create condition types
    create_condition_type(SBSConditions.BEAM_ENERGY, ConditionType.FLOAT_FIELD, "GeV")
    create_condition_type(SBSConditions.BEAM_CURRENT, ConditionType.FLOAT_FIELD, "Avg. beam current in uA")
    create_condition_type(SBSConditions.TARGET, ConditionType.STRING_FIELD)
    create_condition_type(SBSConditions.BB_ANGLE, ConditionType.FLOAT_FIELD, "BB angle in deg")
    create_condition_type(SBSConditions.SBS_ANGLE, ConditionType.FLOAT_FIELD, "SBS angle in deg")
    create_condition_type(SBSConditions.BB_CURRENT, ConditionType.FLOAT_FIELD, "BB current set value in A")
    create_condition_type(SBSConditions.SBS_CURRENT, ConditionType.FLOAT_FIELD, "SBS current set value in A")
