from flask import Blueprint, jsonify, request
from src.models.user import User, db
from sqlalchemy.exc import IntegrityError
import logging

user_bp = Blueprint('user', __name__)
logger = logging.getLogger(__name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Obtiene todos los usuarios"""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users]
        })
    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Crea un nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se enviaron datos'
            }), 400
        
        # Validar campos requeridos
        if 'username' not in data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Username y email son requeridos'
            }), 400
        
        user = User(
            username=data['username'].strip(),
            email=data['email'].strip().lower()
        )
        
        # Validar datos
        validation_errors = user.validate()
        if validation_errors:
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'details': validation_errors
            }), 400
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Username o email ya existe'
        }), 409
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creando usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obtiene un usuario específico"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        logger.error(f"Error obteniendo usuario {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Actualiza un usuario existente"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se enviaron datos'
            }), 400
        
        # Actualizar campos si se proporcionan
        if 'username' in data:
            user.username = data['username'].strip()
        if 'email' in data:
            user.email = data['email'].strip().lower()
        
        # Validar datos actualizados
        validation_errors = user.validate()
        if validation_errors:
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'details': validation_errors
            }), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Username o email ya existe'
        }), 409
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error actualizando usuario {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Elimina un usuario"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario eliminado correctamente'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error eliminando usuario {user_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
