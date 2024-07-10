from flask import request, jsonify
from infraestructure.controllers.cloth_controller import ClothController
from infraestructure.controllers.period_controller import PeriodController
from infraestructure.controllers.status_controller import StatusController

def create_routes(app, mongo):

    cloth_controller = ClothController(mongo)
    period_controller = PeriodController(mongo)
    status_controller = StatusController(mongo)

    @app.route('/status', methods=['POST'])
    def create_status():
        return status_controller.create_status(request.json)

    @app.route('/status/<id>', methods=['GET'])
    def get_status(id):
        return status_controller.get_status(id)

    @app.route('/status/<id>', methods=['PUT'])
    def update_status(id):
        return status_controller.update_status(id, request.json)

    @app.route('/status/<id>', methods=['DELETE'])
    def delete_status(id):
        return status_controller.delete_status(id)

    @app.route('/cloth', methods=['POST'])
    def create_cloth():
        return cloth_controller.create_cloth(request.json)

    @app.route('/cloth/<id>', methods=['GET'])
    def get_cloth(id):
        return cloth_controller.get_cloth(id)

    @app.route('/cloth/<id>', methods=['PUT'])
    def update_cloth(id):
        return cloth_controller.update_cloth(id, request.json)

    @app.route('/cloth/<id>', methods=['DELETE'])
    def delete_cloth(id):
        return cloth_controller.delete_cloth(id)

    @app.route('/cloth/type/<type>', methods=['GET'])
    def get_cloth_by_type(type):
        return cloth_controller.get_cloth_by_type(type)

    @app.route('/cloth/status/<status>', methods=['GET'])
    def get_cloth_by_status(status):
        return cloth_controller.get_cloth_by_status(status)

    @app.route('/period', methods=['POST'])
    def create_period():
        return period_controller.create_period(request.json)

    @app.route('/period/<id>', methods=['GET'])
    def get_period(id):
        return period_controller.get_period(id)

    @app.route('/period/<id>', methods=['PUT'])
    def update_period(id):
        return period_controller.update_period(id, request.json)

    @app.route('/period/<id>', methods=['DELETE'])
    def delete_period(id):
        return period_controller.delete_period(id)

    @app.route('/period/<id>/cloth/count', methods=['GET'])
    def get_period_cloth_count(id):
        return period_controller.get_period_cloth_count(id)

    @app.route('/period/<id>/cloth/list', methods=['GET'])
    def get_period_cloth_list(id):
        return period_controller.get_period_cloth_list(id)
