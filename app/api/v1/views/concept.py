"""
    This module deals with how the concept data is displayed.
"""
import datetime
from flask_restplus import Resource, reqparse, Api
from flask_jwt_extended import jwt_required
from flask import request, jsonify,Flask
from app.api.v1.models.users import UserModel
from app.api.v1.models.concept import ConceptsModel
from app.api.v1.validators.validators import Validate

class Concepts(Resource):
    """
        This class implements the view for POST and GET ALL for concepts
    """

    @jwt_required
    def post(self):
        """
            This view implements the post request and saves the concept to the database
        """
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("concept_name",
                            type=str,
                            required=True,
                            help="Concept name is required.")

        parser.add_argument("concept_item",
                            type=str,
                            required=True,
                            help="Concept item is required.")
        
        parser.add_argument("concept_image",
                            type=str,
                            help="Concept image is optional.")

        parser.add_argument("concept_category",
                            type=str,
                            required=True,
                            help="Concept category is required.")
        
        parser.add_argument("concept_mood",
                            type=str,
                            help="Concept mood is optional.")

        parser.add_argument("concept_audience",
                            type=str,
                            help="Concept audience is optional.")

        parser.add_argument("concept_platform",
                            type=str,
                            help="Concept platform is optional.")

        Valid = Validate()
        args = parser.parse_args()

        concept_name =args.get("concept_name").strip()
        concept_item =args.get("concept_item").strip()
        concept_image = args.get("concept_image").strip()
        concept_category =args.get("concept_category").strip()
        concept_mood =args.get("concept_mood").strip()
        concept_audience =args.get("concept_audience").strip()
        concept_platform =args.get("concept_platform").strip()
        self.model = ConceptsModel(concept_name=concept_name, concept_item=concept_item,
                                    concept_image=concept_image, concept_category=concept_category,
                                    concept_mood=concept_mood, concept_audience=concept_audience, 
                                    concept_platform=concept_platform)

        if not request.json:
            return jsonify({"error": "Make sure your request type is application/json"})
        if not Valid.valid_string(concept_name) or not bool(concept_name):
            return {"error": "Concept name is invalid or empty",
                    "hint": "Concept name should be a sting"},400
        if not Valid.valid_string(concept_item) or not bool(concept_item):
            return {"error": "Concept item is invalid or empty",
                    "hint": "Concept item should be a sting"},400
        #TODO VALIDATE LINK
        if not Valid.valid_string(concept_image) or not bool(concept_image):
            return {"error": "Concept image is invalid or empty",
                    "hint": "Concept image should be a link"},400
        if not Valid.valid_string(concept_category) or not bool(concept_category):
            return {"error": "Concept category is invalid or empty",
                    "hint": "Concept category should be a sting"},400
        if not Valid.valid_string(concept_mood) or not bool(concept_mood):
            return {"error": "Concept mood is invalid or empty",
                    "hint": "Concept mood should be a sting"},400
        if not Valid.valid_string(concept_audience) or not bool(concept_audience):
            return {"error": "Concept audience is invalid or empty",
                    "hint": "Concept audience should be a sting"},400
        if not Valid.valid_string(concept_platform) or not bool(concept_platform):
            return {"error": "Concept platfrom is invalid or empty",
                    "hint": "Concept platfrom should be a sting"},400
        #TODO redirect to edit concept
        if self.model.find_concept_by_name(concept_name):
            return {"status": 400, "error":"Concept already exists"},400

        if self.model.save_concept_to_database():
            return {
                "status": 201,
                "data": [{
                    "concept": self.model.find_concept_by_name(concept_name), 
                }],
                "message": "Concept created successfully"
            },201

