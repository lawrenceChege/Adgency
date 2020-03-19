"""
    This module deals with how the concept data is displayed.
"""
import datetime
from flask_restplus import Resource, reqparse, Api
from flask_jwt_extended import jwt_required
from flask import request, jsonify, Flask
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

        parser.add_argument("name",
                            type=str,
                            required=True,
                            help="Concept name is required.")

        parser.add_argument("image",
                            type=str,
                            help="Concept image is optional.")

        parser.add_argument("category",
                            type=str,
                            required=True,
                            help="Concept category is required.")

        parser.add_argument("overview",
                            type=str,
                            help="Concept overview is optional.")

        parser.add_argument("tone",
                            type=str,
                            help="Concept tone is optional.")

        parser.add_argument("style",
                            type=str,
                            help="Concept style is optional.")

        parser.add_argument("duration",
                            type=str,
                            help="Concept duration is optional.")
        parser.add_argument("project",
                            type=str,
                            required=True,
                            help="Concept project is required.")

        Valid = Validate()
        args = parser.parse_args()

        # Request data
        

        data = { 
            "name": args.get("name").strip(),
            "image": args.get("image").strip(),
            "category" : args.get("category").strip(),
            "overview" : args.get("overview").strip(),
            "tone" : args.get("tone").strip(),
            "style": args.get("style").strip(),
            "duration" : args.get("duration").strip(),
            "project" : args.get("project").strip()
            }
            

        # Connecting to data models
        self.model = ConceptsModel()

        if not request.json:
            return jsonify({"error": "Make sure your request type is application/json"})
        if not Valid.valid_string(data["name"]) or not bool(data["name"]):
            return {"error": "Concept name is invalid or empty",
                    "hint": "Concept name should be a string"}, 400
        #TODO VALIDATE LINK
        if not Valid.valid_string(data["image"]) or not bool(data["image"]):
            return {"error": "Concept image is invalid or empty",
                    "hint": "Concept image should be a link"}, 400
        if not Valid.valid_string(data["category"]) or not bool(data["category"]):
            return {"error": "Concept category is invalid or empty",
                    "hint": "Concept category should be a string"}, 400

        if not Valid.valid_string(data["overview"]) or not bool(data["overview"]):
            return {"error": "Concept overview is invalid or empty",
                    "hint": "Concept category should be a string"}, 400

        if not Valid.valid_string(data["tone"]) or not bool(data["tone"]):
            return {"error": "Concept tone is invalid or empty",
                    "hint": "Concept tone should be a string"}, 400
        if not Valid.valid_string(data["style"]) or not bool(data["style"]):
            return {"error": "Concept style is invalid or empty",
                    "hint": "Concept style should be a string"}, 400
        if not Valid.valid_string(data["duration"]) or not bool(data["duration"]):
            return {"error": "Concept duration is invalid or empty",
                    "hint": "Concept duration should be a string"}, 400
        if not Valid.valid_string(data["project"]) or not bool(data["project"]):
            return {"error": "Concept project is invalid or empty",
                    "hint": "Concept project should be a string"}, 400

        #TODO redirect to edit concept
        if self.model.find_concept_by_name(data["name"]):
            return {"status": 400, "error": "Concept already exists"}, 400

        try:
            self.model.save_concept_to_database(**data)
            return {
                "status": 201,
                "data": [{
                    "concept": data["name"],
                }],
                "message": "Concept created successfully"
            }, 201

        except Exception as error:
            print(error)
            return {"status": 500, "error": "oops! Something went wrong :-("}, 400

    def get(self):
        """
            This method retrives all the posted concepts from the database
        """
        self.model = ConceptsModel()
        concepts = self.model.get_all_concepts()
        if Concepts:
            return {"status": 200,
                    "data": [{
                        "All concepts": concepts
                    }],
                    "message": "All concepts found successfully"}, 200
        return {"status": 404, "message": 'No concepts found'}, 404


class Concept(Resource):
    """
        This class holds methods for single concepts
    """

    def get(self, concept_id):
        """
            This method retrieves a conceptfrom the database using its id
        """
        self.model = ConceptsModel()
        concept = self.model.find_concept_by_id(concept_id)
        if not concept:
            return {"status": 404, "error": "Concept not found"}, 404
        return {"status": 200,
                "data": [
                    {
                        "concept": concept,
                    }
                ],
                "message": "Concept successfully retrieved!"}, 200

    @jwt_required
    def put(self, concept_id):
        """
            This method modifies a concept partially or wholly
        """
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("name",
                            type=str,
                            required=True,
                            help="Concept name is required.")

        parser.add_argument("image",
                            type=str,
                            help="Concept image is optional.")

        parser.add_argument("category",
                            type=str,
                            required=True,
                            help="Concept category is required.")

        parser.add_argument("overview",
                            type=str,
                            help="Concept overview is optional.")

        parser.add_argument("tone",
                            type=str,
                            help="Concept tone is optional.")

        parser.add_argument("style",
                            type=str,
                            help="Concept style is optional.")

        parser.add_argument("duration",
                            type=str,
                            help="Concept duration is optional.")

        Valid = Validate()
        args = parser.parse_args()

        data = { 
            "name": args.get("name").strip(),
            "image": args.get("image").strip(),
            "category" : args.get("category").strip(),
            "overview" : args.get("overview").strip(),
            "tone" : args.get("tone").strip(),
            "style": args.get("style").strip(),
            "duration" : args.get("duration").strip()
            }
        self.model = ConceptsModel()

        if not request.json:
            return jsonify({"error": "Make sure your request type is application/json"})
        if not Valid.valid_string(data["name"]) or not bool(data["name"]):
            return {"error": "Concept name is invalid or empty",
                    "hint": "Concept name should be a string"}, 400
        #TODO VALIDATE LINK
        if not Valid.valid_string(data["image"]) or not bool(data["image"]):
            return {"error": "Concept image is invalid or empty",
                    "hint": "Concept image should be a link"}, 400
        if not Valid.valid_string(data["category"]) or not bool(data["category"]):
            return {"error": "Concept category is invalid or empty",
                    "hint": "Concept category should be a string"}, 400

        if not Valid.valid_string(data["overview"]) or not bool(data["overview"]):
            return {"error": "Concept overview is invalid or empty",
                    "hint": "Concept category should be a string"}, 400

        if not Valid.valid_string(data["tone"]) or not bool(data["tone"]):
            return {"error": "Concept tone is invalid or empty",
                    "hint": "Concept tone should be a string"}, 400
        if not Valid.valid_string(data["style"]) or not bool(data["style"]):
            return {"error": "Concept style is invalid or empty",
                    "hint": "Concept style should be a string"}, 400
        if not Valid.valid_string(data["duration"]) or not bool(data["duration"]):
            return {"error": "Concept duration is invalid or empty",
                    "hint": "Concept duration should be a string"}, 400
        #TODO redirect to edit concept
        if not self.model.find_concept_by_id(concept_id):
            return {"status": 400, "error": "Concept not found"}, 404


        concept = self.model.edit_concept(concept_id, **data)
        if not concept:
            print(concept)
            return {"status": 302, "error": "Concept not updated"}, 302
        return {"status": 200,
                "data": [
                    {
                        "concept": self.model.find_concept_by_id(concept_id),
                    }
                ],
                "message": "Concept updated successfully!"}, 200

    @jwt_required
    def delete(self, concept_id):
        """
            This method removes a concept from the db
        """
        self.model = ConceptsModel()
        if not self.model.find_concept_by_id(concept_id):
            return {"status": 400, "error": "Concept not found"}, 404
        
        if self.model.delete_concept(concept_id) :
            return {"status": 200,
                    "data": [
                        {
                            "Conncept id": concept_id,
                        }
                    ],
                    "message": "Concept successfuly deleted"}, 200
