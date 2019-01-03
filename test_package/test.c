#include <pjsua-lib/pjsua.h>

int main() {
    pj_status_t status;
    pjsua_state pj_state;

     /* Create pjsua first! */
    pj_state = pjsua_get_state();
    if (pj_state == PJSUA_STATE_NULL) {
        printf("Creating PJSUA\n");
        status = pjsua_create();
        if (status != PJ_SUCCESS) return EXIT_FAILURE;
    } else {
        printf("PJSUA already created\n");
    }
    /* Init pjsua */
    {
    const pjsua_config cfg;
    const pjsua_logging_config log_cfg;

    pjsua_config_default(&cfg);
//     cfg.cb.on_incoming_call = &on_incoming_call;
//     cfg.cb.on_call_media_state = &on_call_media_state;
//     cfg.cb.on_call_state = &on_call_state;

    pjsua_logging_config_default(&log_cfg);
    log_cfg.console_level = 4;

    status = pjsua_init(&cfg, &log_cfg, NULL);
    if (status != PJ_SUCCESS) return EXIT_FAILURE;
    }

    /* Add UDP transport. */
    {
    const pjsua_transport_config cfg;

    pjsua_transport_config_default(&cfg);
    cfg.port = 5063;
    status = pjsua_transport_create(PJSIP_TRANSPORT_UDP, &cfg, NULL);
    if (status != PJ_SUCCESS) return EXIT_FAILURE;
    }

    /* Initialization is done, now start pjsua */
    status = pjsua_start();
    if (status != PJ_SUCCESS) return EXIT_FAILURE;
    
    status = pjsua_destroy();
    if (status != PJ_SUCCESS) return EXIT_FAILURE;

    return EXIT_SUCCESS;
}
