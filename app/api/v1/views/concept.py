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

        concept_name = args.get("concept_name").strip()
        concept_item = args.get("concept_item").strip()
        concept_image = args.get("concept_image").strip()
        concept_category = args.get("concept_category").strip()
        concept_mood = args.get("concept_mood").strip()
        concept_audience = args.get("concept_audience").strip()
        concept_platform = args.get("concept_platform").strip()
        self.model = ConceptsModel(concept_name=concept_name, concept_item=concept_item,
                                   concept_image=concept_image, concept_category=concept_category,
                                   concept_mood=concept_mood, concept_audience=concept_audience,
                                   concept_platform=concept_platform)

        if not request.json:
            return jsonify({"error": "Make sure your request type is application/json"})
        if not Valid.valid_string(concept_name) or not bool(concept_name):
            return {"error": "Concept name is invalid or empty",
                    "hint": "Concept name should be a sting"}, 400
        if not Valid.valid_string(concept_item) or not bool(concept_item):
            return {"error": "Concept item is invalid or empty",
                    "hint": "Concept item should be a sting"}, 400
        #TODO VALIDATE LINK
        if not Valid.valid_string(concept_image) or not bool(concept_image):
            return {"error": "Concept image is invalid or empty",
                    "hint": "Concept image should be a link"}, 400
        if not Valid.valid_string(concept_category) or not bool(concept_category):
            return {"error": "Concept category is invalid or empty",
                    "hint": "Concept category should be a sting"}, 400
        if not Valid.valid_string(concept_mood) or not bool(concept_mood):
            return {"error": "Concept mood is invalid or empty",
                    "hint": "Concept mood should be a sting"}, 400
        if not Valid.valid_string(concept_audience) or not bool(concept_audience):
            return {"error": "Concept audience is invalid or empty",
                    "hint": "Concept audience should be a sting"}, 400
        if not Valid.valid_string(concept_platform) or not bool(concept_platform):
            return {"error": "Concept platfrom is invalid or empty",
                    "hint": "Concept platfrom should be a sting"}, 400
        #TODO redirect to edit concept
        if self.model.find_concept_by_name(concept_name):
            return {"status": 400, "error": "Concept already exists"}, 400

        if self.model.save_concept_to_database():
            return {
                "status": 201,
                "data": [{
                    "concept": self.model.find_concept_by_name(concept_name),
                }],
                "message": "Concept created successfully"
            }, 201

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
                    "message": "All conceptss found successfully"}, 200
        return {"status": 404, "message": 'No conceptss found'}, 404


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
    def put(self, incident_id):
        """
            This method modifies an incident partially or wholly
        """
        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("title",
                            type=str,
                            required=True,
                            help="title field is required.")
        parser.add_argument("comment",
                            type=str,
                            required=True,
                            help="comment field is required.")
        parser.add_argument("IncidentType",
                            type=str,
                            help="Type field is required.")
        parser.add_argument("images",
                            type=str,
                            help="images field is optional.")
        parser.add_argument("video",
                            type=str,
                            help="video field is optional.")
        parser.add_argument("location",
                            type=str,
                            help="location field is optional.")
        Valid = Validate()
        self.model = IncidentsModel()
        args = parser.parse_args()
        title = args.get("title")
        images = args.get("images")
        video = args.get("video")
        location = args.get("location")
        comment = args.get("comment")
        if not request.json:
            return {"error": "check your request type"}, 400

        if not Valid.valid_string(title) or not bool(title.strip()):
            return {"error": "Title is invalid or empty"}, 400

        if not Valid.valid_string(images) or not bool(images):
            return {"error": "Images link is invalid"}, 400

        if not Valid.valid_string(video)or not bool(video):
            return {"error": "Video link is invalid"}, 400

        if not Valid.valid_string(location) or not bool(location):
            return {"error": "location input  is invalid"}, 400

        if not Valid.valid_string(comment) or not bool(comment.strip()):
            return {"error": "comment is invalid or empty"}, 400

        incident = self.model.get_incident_by_id(incident_id)
        if not incident:
            return {"status": 404, "error": "Incindent not found"}, 404

        createdby = incident.get('createdby')
        user = self.model.current_user()
        if user != createdby:
            return {'status': 403, "error": "This action is forbidden.",
                    'message': ' You are trying to modify someone else post'}

        if not self.model.check_incident_status(incident_id):
            return {'status': 403, "error": "This action is forbidden"}

        if self.model.edit_incident(location, images, video, title, comment, incident_id):
            return {"status": 200,
                    "data": [
                        {
                            "incident": incident_id,
                        }
                    ],
                    "message": "Incident updated successfully!"}, 200

    @jwt_required
    def delete(self, incident_id):
        """
            This method removes an incident from the db
        """
        self.model = IncidentsModel()
        incident = self.model.get_incident_by_id(incident_id)
        if not incident:
            return {"status": 404, "error": "Incident not found"}, 404

        createdby = incident.get('createdby')
        user = self.model.current_user()

        if not self.model.check_incident_status(incident_id):
            return {'status': 403, "error": "This action is forbidden."}
        if user != createdby:
            return {'status': 403, "error": "This action is forbidden.",
                    'message': ' You are trying to delete someone else post'}

        if self.model.delete_incident(incident_id):
            return {"status": 200,
                    "data": [
                        {
                            "incident": incident_id,
                        }
                    ],
                    "message": "Incident successfuly deleted"}, 200
