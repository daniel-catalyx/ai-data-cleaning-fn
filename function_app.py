import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="ResponseProcessor", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
def ResponseProcessor(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get the request body
        req_body = req.get_json()
        
        if not req_body:
            return func.HttpResponse(
                json.dumps({"error": "Please pass a valid JSON payload in the request body"}),
                status_code=400,
                headers={'Content-Type': 'application/json'}
            )
        
        # Validate required fields
        required_fields = ['webhook_name', 'data']
        for field in required_fields:
            if field not in req_body:
                return func.HttpResponse(
                    json.dumps({"error": f"Missing required field: {field}"}),
                    status_code=400,
                    headers={'Content-Type': 'application/json'}
                )
        
        # Extract data from the payload
        webhook_name = req_body.get('webhook_name')
        data = req_body.get('data')
        
        # Log the received data
        logging.info(f"Webhook: {webhook_name}")
        logging.info(f"Session ID: {data.get('session_id')}")
        logging.info(f"Response ID: {data.get('response_id')}")
        logging.info(f"Survey ID: {data.get('survey_id')}")
        logging.info(f"Account ID: {data.get('account_id')}")
        logging.info(f"Response Status: {data.get('response_status')}")
        logging.info(f"Is Test: {data.get('is_test')}")
        
        # Process the data here
        # Add your data cleaning logic
        processed_data = process_survey_response(data)
        
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "message": "Survey response processed successfully",
                "processed_data": processed_data,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }),
            status_code=200,
            headers={'Content-Type': 'application/json'}
        )
        
    except ValueError as ve:
        logging.error(f"JSON parsing error: {str(ve)}")
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON format"}),
            status_code=400,
            headers={'Content-Type': 'application/json'}
        )
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": f"Internal server error: {str(e)}"}),
            status_code=500,
            headers={'Content-Type': 'application/json'}
        )

def process_survey_response(data):
    """
    Process the survey response data
    Add your data cleaning and processing logic here
    """
    try:
        # Extract key information
        session_id = data.get('session_id')
        response_id = data.get('response_id')
        survey_id = data.get('survey_id')
        account_id = data.get('account_id')
        response_status = data.get('response_status')
        is_test = data.get('is_test', False)
        url_variables = data.get('url_variables', [])
        survey_link = data.get('survey_link', [])
        contact = data.get('contact', [])
        
        # Example processing logic
        processed_result = {
            "session_id": session_id,
            "response_id": response_id,
            "survey_id": survey_id,
            "account_id": account_id,
            "status": response_status,
            "is_test_data": is_test,
            "url_variables_count": len(url_variables),
            "survey_link_count": len(survey_link),
            "contact_count": len(contact),
            "processed_at": datetime.datetime.utcnow().isoformat(),
            "cleaning_status": "completed"
        }
        
        # Add your specific data cleaning logic here
        # For example:
        # - Data validation
        # - Data transformation
        # - Database operations
        # - External API calls
        # - Clean and standardize contact information
        # - Process URL variables
        # - Validate survey responses
        
        logging.info(f"Successfully processed response {response_id} for survey {survey_id}")
        
        return processed_result
        
    except Exception as e:
        logging.error(f"Error in process_survey_response: {str(e)}")
        raise