import cv2
import extras.face_crop as cropper


img = cv2.imread('lena.png')
result = cropper.crop_image(img)
cv2.imwrite('lena_result.png', result)
# oldmonk/mcmbuddy.py

import json

def run_mcm_buddy(input_data):
    """
    Main function to process input JSON data, parse and validate each section.
    """
    # Parse and validate 'sim_data'
    sim_data = input_data.get("sim_data", {})
    sim_number = sim_data.get("sim_number")
    fbn = sim_data.get("fbn")
    title = sim_data.get("title")
    description = sim_data.get("description")

    # Check if essential fields in sim_data are missing
    if not sim_number or not fbn or not title or not description:
        return {
            "status": "failure",
            "error": "Missing required fields in 'sim_data'"
        }
    
    # Parse and validate 'cutsheet_data'
    cutsheet_data = input_data.get("cutsheet_data", {})
    hostname = cutsheet_data.get("hostname")
    location = cutsheet_data.get("location")
    state = cutsheet_data.get("state")

    if not hostname or not location or not state:
        return {
            "status": "failure",
            "error": "Missing required fields in 'cutsheet_data'"
        }
    
    # Parse and validate 'additional_data'
    additional_data = input_data.get("additional_data", {})
    site_name = additional_data.get("site_name")
    az_name = additional_data.get("az_name")
    mcm_template_type = additional_data.get("mcm_template_type")
    scope_type = additional_data.get("scope_type")
    team_name = additional_data.get("team_name")
    cutsheet_type = additional_data.get("cutsheet_type")
    other_fields = additional_data.get("other_fields", {})

    if not site_name or not az_name or not mcm_template_type or not scope_type or not team_name or not cutsheet_type:
        return {
            "status": "failure",
            "error": "Missing required fields in 'additional_data'"
        }

    # Return a success message with parsed data to confirm all fields are accessible
    return {
        "status": "success",
        "sim_data": {
            "sim_number": sim_number,
            "fbn": fbn,
            "title": title,
            "description": description
        },
        "cutsheet_data": {
            "hostname": hostname,
            "location": location,
            "state": state
        },
        "additional_data": {
            "site_name": site_name,
            "az_name": az_name,
            "mcm_template_type": mcm_template_type,
            "scope_type": scope_type,
            "team_name": team_name,
            "cutsheet_type": cutsheet_type,
            "other_fields": other_fields
        },
        "message": "Basic JSON parsing and validation complete"
    }


# oldmonk/__init__.py

import json
from oldmonk.mcmbuddy import run_mcm_buddy

def handler(event, context):
    # Parse JSON input from the event body
    try:
        input_data = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format"})
        }
    
    # Call mcmbuddy function with the parsed JSON
    response = run_mcm_buddy(input_data)
    
    # Return the response from mcmbuddy
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }



{
  "sim_data": {
    "sim_number": "1234567890",
    "fbn": "FBN-123",
    "title": "Network Upgrade",
    "description": "Upgrading network infrastructure in AZ-1"
  },
  "cutsheet_data": {
    "hostname": "host123.example.com",
    "location": "DataCenter-1",
    "state": "Active"
  },
  "additional_data": {
    "site_name": "ExampleSite",
    "az_name": "AZ-1",
    "mcm_template_type": "TemplateA",
    "scope_type": "ScopeX",
    "team_name": "TeamY",
    "cutsheet_type": "TypeB",
    "other_fields": {
      "field1": "value1",
      "field2": "value2"
    }
  }
}
