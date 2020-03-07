"""
    This module deals with how the insight data is displayed.
"""
import datetime
from flask_restplus import Resource, reqparse, Api
from flask_jwt_extended import jwt_required
from flask import request, jsonify, Flask
from app.api.v1.models.users import UserModel
from app.api.v1.models.insights import InsightsModel
from app.api.v1.validators.validators import Validate


class Insights(Resource):
    """
        This class implements the view for POST and GET ALL for insights
    """

    @jwt_required
    def post(self):
        """
            This view implements the post request and saves the insight to the database
        """
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("insight",
                            type=str,
                            help="insight is optional.")

        Valid = Validate()
        args = parser.parse_args()

        data = args.get("insight").strip()
        self.model = InsightsModel()

        if not request.json:
            return jsonify({"error": "Make sure your request type is application/json"})
        if not Valid.valid_string(data) or not bool(data):
            return {"error": "insight is invalid or empty",
                    "hint": "insight should be a string"}, 400
         #TODO redirect to edit insight
        if self.model.find_insight(data):
            return {"status": 400, "error": "insight already exists"}, 400

        if self.model.save_insight_to_database(data):
            return {
                "status": 201,
                "data": [{
                    "insight": self.model.find_insight(data),
                }],
                "message": "insight created successfully"
            }, 201

    def get(self):
        """
            This method retrives all the posted insights from the database
        """
        self.model = InsightsModel()
        insights = self.model.get_all_insights()
        if insights:
            return {"status": 200,
                    "data": [{
                        "All insights": insights
                    }],
                    "message": "All insights found successfully"}, 200
        return {"status": 404, "message": 'No insights found'}, 404


class Insight(Resource):
    """
        This class holds methods for single insights
    """

    def get(self, insight_id):
        """
            This method retrieves a insightfrom the database using its id
        """
        self.model = InsightsModel()
        insight = self.model.find_insight_by_id(insight_id)
        if not insight:
            return {"status": 404, "error": "insight not found"}, 404
        return {"status": 200,
                "data": [
                    {
                        "insight": insight,
                    }
                ],
                "message": "insight successfully retrieved!"}, 200

    @jwt_required
    def put(self, insight_id):
        """
            This method modifies a insight partially or wholly
        """
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("insight",
                            type=str,
                            help="insight is optional.")

        Valid = Validate()
        args = parser.parse_args()

        data = args.get("insight").strip()
        self.model = InsightsModel()

        if not request.json:
            return jsonify({"error": "Make sure your request type is application/json"})
        if not Valid.valid_string(data) or not bool(data):
            return {"error": "insight is invalid or empty",
                    "hint": "insight should be a string"}, 400
         #TODO redirect to edit insight
        if not self.model.find_insight_by_id(insight_id):
            return {"status": 400, "error": "insight not found"}, 404


        insight = self.model.edit_insight(insight_id, data)
        if not insight:
            print(insight)
            return {"status": 302, "error": "insight not updated"}, 302
        return {"status": 200,
                "data": [
                    {
                        "insight": self.model.find_insight_by_id(insight_id),
                    }
                ],
                "message": "insight updated successfully!"}, 200

    @jwt_required
    def delete(self, insight_id):
        """
            This method removes a insight from the db
        """
        self.model = InsightsModel()
        if not self.model.find_insight_by_id(insight_id):
            return {"status": 400, "error": "insight not found"}, 404
        
        if self.model.delete_insight(insight_id) :
            return {"status": 200,
                    "data": [
                        {
                            "Conncept id": insight_id,
                        }
                    ],
                    "message": "insight successfuly deleted"}, 200
