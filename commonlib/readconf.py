import sys
import copy
import commonlib.helpers

tostderr = lambda msg: sys.stderr.write(msg + '\n')

def parse_config():
    import conf_default
    try:
        import conf_local
    except Exception, err:
        tostderr("Error: Failed reading local config")
        tostderr("Message: " + str(err))
        tostderr("Hint: Please create local config file conf_local.py")
        sys.exit(1)

    return merge_confs(conf_default, conf_local)

def merge_confs(conf_default, conf_local=None):
    config = commonlib.helpers.odict(**copy.deepcopy(conf_default.config))
    if conf_local:
        local_config = conf_local.config
        for section in config:
            local_config_section = local_config.get(section)
            if local_config_section:
                if isinstance(local_config_section, dict):
                    config[section].update(local_config_section)
                else:
                    config[section] = local_config_section
    return config
