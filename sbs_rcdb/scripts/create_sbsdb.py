import os
import rcdb
import sbsdb

if __name__=="__main__":

    con_str = os.environ["RCDB_CONNECTION"] \
        if "RCDB_CONNECTION" in os.environ.keys() \
        else "mysql://rcdb@localhost/test"

    """
    Connect and create default tables
    CAUTION: it will delete existing schema and create a new one
    """
    db = rcdb.RCDBProvider(con_str, check_version=False)
    #comment out: db is initially empty
    rcdb.provider.destroy_all_create_schema(db)

    print("create default condition types")
    rcdb.create_condition_types(db)

    #print("add experiment specific condition types")
    sbsdb.create_condition_types(db)

    """
    v = SchemaVersion()
    v.version = rcdb.SQL_SCHEMA_VERSION
    v.comment = "CREATED BY get_started script"
    db.session.add(v)
    db.session.commit()
    """
