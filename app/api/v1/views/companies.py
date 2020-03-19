"""
    This module holds the views for the users
"""
from flask_restplus import Resource, reqparse, Api
from flask_jwt_extended import (jwt_required, get_jwt_identity,
 jwt_refresh_token_required, get_raw_jwt, create_access_token)
from flask import request, Flask, jsonify
from app.api.v1.models.companies import companiesModel
from app.api.v1.validators.validators import Validate
from app.api.v1.models.users import UserModel

app = Flask(__name__)
api = Api(app)


class Companies(Resource):
    """
        This class defines methods for companies
    """

    @api.doc(params={
                    'copany_name': 'Enter a unique copany_name',
                    'email': 'Enter email',
                    'is_client': 'client?'
                    })

    @jwt_required
    def post(self):
        """
            This method registers a user to the database.
        """

        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("company_name",
                            type=str,
                            required=True,
                            help="company field is required.")
        parser.add_argument("is_client",
                            type=bool,
                            required=True,
                            help="Role field is required.")
        
        parser.add_argument("email",
                            type=str,
                            help="Email field is optional.")

        args = parser.parse_args()
        Valid = Validate()
        data = { 
            "company_name": args.get("company_name").strip(),
            "email": args.get("email").strip(),
            "is_client" : args.get("is_client")          
            }

        # Connecting to data models
        self.model = companiesModel()

        if not request.json:
            return jsonify({"error": "Make sure your request type is application/json"})
        if not Valid.valid_string(data["company_name"]) or not bool(data["company_name"]):
            return {"error": "Company name is invalid or empty",
                    "hint": "Company name should be a string"}, 400
        #TODO VALIDATE LINK
        if not Valid.valid_string(data["email"]) or not bool(data["email"]):
            return {"error": "Company email is invalid or empty",
                    "hint": "Company email should be a string"}, 400

        #TODO redirect to edit company
        if self.model.find_company_by_name(data["company_name"]):
            return {"status": 400, "error": "Company already exists"}, 400

        try:
            self.model.save_company_to_database(**data)
            company = self.model.find_company_by_name(data["company_name"])
            # UserModel().uplink_company(company["company_id"], get_jwt_identity())
            return {
                "status": 201,
                "data": [{
                    "company": company,
                }],
                "message": "Company created successfully"
            }, 201

        except Exception as error:
            print(error)
            return {"status": 500, "error": "oops! Something went wrong :-("}, 400

    def get(self):
        """
            This method retrives all the posted companies from the database
        """
        self.model = companiesModel()
        companies = self.model.get_all_companies()
        if companies:
            return {"status": 200,
                    "data": [{
                        "All companies": companies
                    }],
                    "message": "All companies found successfully"}, 200
        return {"status": 404, "message": 'No companies found'}, 404


class Company(Resource):
    """
        This class holds methods for single companies
    """

    def get(self, company_id):
        """
            This method retrieves a conceptfrom the database using its id
        """
        self.model = companiesModel()
        company = self.model.find_company_by_id(company_id)
        if not company:
            return {"status": 404, "error": "Company not found"}, 404
        return {"status": 200,
                "data": [
                    {
                        "company": company,
                    }
                ],
                "message": "Company successfully retrieved!"}, 200

    @jwt_required
    def put(self, company_id):
        """
            This method modifies a company partially or wholly
        """
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("copany_name",
                            type=str,
                            required=True,
                            help="company field is required.")
        parser.add_argument("is_client",
                            type=bool,
                            required=True,
                            help="Role field is required.")
        
        parser.add_argument("email",
                            type=str,
                            help="Email field is optional.")

        args = parser.parse_args()
        Valid = Validate()
        data = { 
            "company_name": args.get("company_name").strip(),
            "email": args.get("email").strip(),
            "is_client" : args.get("is_client").strip()            
            }

        # Connecting to data models
        self.model = companiesModel()

        if not request.json:
            return jsonify({"error": "Make sure your request type is application/json"})
        if not Valid.valid_string(data["company_name"]) or not bool(data["company_name"]):
            return {"error": "Company name is invalid or empty",
                    "hint": "Company name should be a string"}, 400
        #TODO VALIDATE LINK
        if not Valid.valid_string(data["email"]) or not bool(data["email"]):
            return {"error": "Company email is invalid or empty",
                    "hint": "Company email should be a string"}, 400
        #TODO redirect to edit company
        if not self.model.find_company_by_id(company_id):
            return {"status": 400, "error": "Company not found"}, 404


        company = self.model.edit_company(company_id, **data)
        if not company:
            print(company)
            return {"status": 302, "error": "Company not updated"}, 302
        return {"status": 200,
                "data": [
                    {
                        "company": self.model.find_company_by_id(company_id),
                    }
                ],
                "message": "Company updated successfully!"}, 200

    @jwt_required
    def delete(self, company_id):
        """
            This method removes a company from the db
        """
        self.model = companiesModel()
        if not self.model.find_company_by_id(company_id):
            return {"status": 400, "error": "Company not found"}, 404
        
        if self.model.delete_company(company_id) :
            return {"status": 200,
                    "data": [
                        {
                            "Conncept id": company_id,
                        }
                    ],
                    "message": "Company successfuly deleted"}, 200
