import json
import os

def create_postman_json(controller_host, controller_port, client_id, account_name, api_token, application_id, duration_in_mins):

    # Define the requests
    get_token_request = {
        "name": "Get API Token",
        "request": {
            "method": "POST",
            "header": [
                {"key": "Content-Type", "value": "application/x-www-form-urlencoded"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/api/oauth/access_token",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "api", "oauth", "access_token"],
                "query": [
                    {"key": "grant_type", "value": "client_credentials"},
                    {"key": "client_id", "value": "{{client_id}}"},
                    {"key": "client_secret", "value": "{{client_secret}}"}
                ]
            }
        }
    }

    get_metric_data_request = {
        "name": "Get Metric Data",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/metric-data",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "metric-data"],
                "query": [
                    {"key": "metric-path", "value": "<add-metric-path>"},
                    {"key": "time-range-type", "value": "BEFORE_NOW"},
                    {"key": "duration-in-mins", "value": duration_in_mins}
                ]
            }
        }
    }

    get_business_transactions_data_request = {
        "name": "Get Business Transactions Data",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/business-transactions",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "business-transactions"],
                "query": [
                    {"key": "time-range-type", "value": "BEFORE_NOW"},
                    {"key": "duration-in-mins", "value": duration_in_mins}
                ]
            }
        }
    }

    get_all_applications_request = {
        "name": "Get All Applications",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications"],
                "query": [
                    {"key": "time-range-type", "value": "BEFORE_NOW"},
                    {"key": "duration-in-mins", "value": duration_in_mins}
                ]
            }
        }
    }

    get_application_business_transactions_request = {
        "name": "Get Application's Business Transactions",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/business-transactions",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "business-transactions"],
                "query": [
                    {"key": "time-range-type", "value": "BEFORE_NOW"},
                    {"key": "duration-in-mins", "value": duration_in_mins}
                ]
            }
        }
    }

    get_application_tiers_request = {
        "name": "Get Application's Tiers",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/tiers",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "tiers"],
            }
        }
    }

    get_application_backends_request = {
        "name": "Get Application's Backends",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/backends",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "backends"],
            }
        }
    }

    get_application_nodes_request = {
        "name": "Get Application's Nodes",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/nodes",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "nodes"],
            }
        }
    }

    get_application_metrics_request = {
        "name": "Get Application's Metrics",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/metrics",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "metrics"],
            }
        }
    }

    get_application_specific_metric_request = {
        "name": "Get Application's Specific Metrics",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/metrics",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "metrics"],
                "query": [
                    {"key": "metric-path", "value": "Overall Application Performance"}
                ]
            }
        }
    }

    get_application_metric_data_request = {
        "name": "Get Application's Metric Data",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/metric-data",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "metric-data"],
                "query": [
                    {"key": "metric-path", "value": "Overall Application Performance|*|*|*|Average Response Time (ms)"},
                    {"key": "time-range-type", "value": "BEFORE_NOW"},
                    {"key": "duration-in-mins", "value": duration_in_mins}
                ]
            }
        }
    }

    get_application_infrastructure_performance_request = {
        "name": "Get Application's Infrastructure Performance",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/metric-data",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "metric-data"],
                "query": [
                    {"key": "metric-path",
                     "value": "Application Infrastructure Performance|*|Individual Nodes|*|*|*|*"},
                    {"key": "time-range-type", "value": "BEFORE_NOW"},
                    {"key": "duration-in-mins", "value": duration_in_mins}
                ]
            }
        }
    }
    get_calls_per_minute_request = {
        "name": "Get Calls per Minute",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/metric-data",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "metric-data"],
                "query": [
                    {"key": "metric-path", "value": "Overall Application Performance|Calls per Minute"},
                    {"key": "time-range-type", "value": "BEFORE_NOW"},
                    {"key": "duration-in-mins", "value": duration_in_mins}
                ]
            }
        }
    }

    get_errors_per_minute_request = {
        "name": "Get Errors per Minute",
        "request": {
            "method": "GET",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": f"Bearer {api_token}"}
            ],
            "url": {
                "raw": f"https://{controller_host}:{controller_port}/controller/rest/applications/{application_id}/metric-data",
                "protocol": "https",
                "host": [controller_host],
                "port": controller_port,
                "path": ["controller", "rest", "applications", application_id, "metric-data"],
                "query": [
                    {"key": "metric-path", "value": "Overall Application Performance|Errors per Minute"},
                    {"key": "time-range-type", "value": "BEFORE_NOW"},
                    {"key": "duration-in-mins", "value": duration_in_mins}
                ]
            }
        }
    }
# Define the Postman collection
    postman_collection = {
        "info": {
            "_postman_id": "f95c8d22-2ac3-4aa0-8349-c77e5d4accdd",
            "name": "AppDynamics API Collection",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            get_token_request,
            get_metric_data_request,
            get_business_transactions_data_request,
            get_all_applications_request,
            get_application_business_transactions_request,
            get_application_tiers_request,
            get_application_backends_request,
            get_application_nodes_request,
            get_application_metrics_request,
            get_application_specific_metric_request,
            get_application_metric_data_request,
            get_application_infrastructure_performance_request,
            get_calls_per_minute_request,
            get_errors_per_minute_request,
        ]
    }

    # Define the environment
    environment = {
        "name": "AppDynamics",
        "values": [
            {
                "key": "client_id",
                "value": f"{client_id}@{account_name}",
                "enabled": True
            },
            {
                "key": "account_name",
                "value": account_name,
                "enabled": True
            },
            {
                "key": "client_secret",
                "type": "secret",
                "enabled": True
            },
            {
                "key": "api_key",
                "type": "string",
                "value": api_token,
                "enabled": True
            }
        ],
        "enabled": True
    }

    # Define the directory where the files will be saved
    results_folder = os.path.expanduser("~/Desktop/appd_api_results")
    os.makedirs(results_folder, exist_ok=True)

    # Save the Postman collection JSON to a file in the results folder
    with open(os.path.join(results_folder, 'appd_api_collection.json'), 'w') as f:
        json.dump(postman_collection, f, indent=4)

    # Save the environment JSON to a file in the results folder
    with open(os.path.join(results_folder, 'appd_api_environment.json'), 'w') as f:
        json.dump(environment, f, indent=4)