from flask import Flask, request, jsonify, send_from_directory
import random

app = Flask(__name__, static_folder='static')


# Класс данных дрона (Model)
class DroneControlSystem:
    """Класс для управления данными дрона, такими, как скорость, высота, координаты и батарея."""

    def __init__(self):
        self.altitude = 0
        self.speed = 0
        self.position = (0, 0)
        self.battery = 100
        self.direction = 0  # направление движения дрона в градусах

    def update_position(self, x, y):
        """Обновление координат дрона."""
        self.position = (x, y)

    def change_altitude(self, altitude):
        """Обновление высоты полета."""
        self.altitude = altitude

    def update_speed(self, speed):
        """Изменение скорости."""
        self.speed = speed

    def change_direction(self, direction):
        """Изменение направления полета."""
        self.direction = direction

    def consume_battery(self, consumption):
        """Понижение уровня заряда батареи."""
        self.battery -= consumption

    def check_battery(self):
        """Возвращение текущего уровня заряда батареи."""
        return self.battery


# Класс представления (View)
class DroneInterface:
    """Класс для отображения информации о дроне и взаимодействия с пользователем."""

    def show_status(self, drone_model):
        """Вывод информации о текущем состоянии дрона."""
        return {
            'altitude': drone_model.altitude,
            'speed': drone_model.speed,
            'position': drone_model.position,
            'battery': drone_model.battery,
            'direction': drone_model.direction
        }

    def display_alert(self, message):
        """Отображение сообщений системы."""
        return {"alert": message}


# Контроллер для управления логикой
class DroneOperations:
    """Контроллер для управления поведением дрона."""

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def adjust_position(self, x, y):
        """Обновление координат дрона."""
        self.model.update_position(x, y)
        return self.view.show_status(self.model)

    def adjust_altitude(self, altitude):
        """Обновление высоты дрона."""
        self.model.change_altitude(altitude)
        return self.view.show_status(self.model)

    def adjust_speed(self, speed):
        """Изменение скорости дрона."""
        self.model.update_speed(speed)
        return self.view.show_status(self.model)

    def adjust_direction(self, direction):
        """Изменение направления дрона."""
        self.model.change_direction(direction)
        return self.view.show_status(self.model)

    def monitor_battery(self):
        """Проверка состояния батареи и возвращение на базу при низком заряде."""
        if self.model.check_battery() < 20:
            return self.view.display_alert("Battery low! Returning to base.")
        return self.view.show_status(self.model)


# Симуляция сенсоров
class SensorSimulation:
    """Класс для симуляции сенсоров и создания виртуальной среды."""

    def simulate_obstacle(self):
        """Симуляция появления препятствия."""
        distance_to_obstacle = random.uniform(0, 50)  # Случайное расстояние до препятствия
        return distance_to_obstacle

    def simulate_weather_conditions(self):
        """Симуляция погодных условий."""
        wind_speed = random.uniform(0, 20)  # Случайная скорость ветра
        weather_conditions = random.choice(["Clear", "Cloudy", "Stormy", "Rainy"])
        return {"wind_speed": wind_speed, "weather": weather_conditions}


# Инициализация дрона и контроллера
drone_model = DroneControlSystem()
drone_view = DroneInterface()
drone_controller = DroneOperations(drone_model, drone_view)
sensor_simulator = SensorSimulation()


# Маршрут для главной страницы
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# API для получения статуса дрона
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(drone_view.show_status(drone_model))


# API для обновления позиции дрона
@app.route('/position', methods=['POST'])
def update_position():
    data = request.get_json()
    x, y = data.get('x', 0), data.get('y', 0)
    return jsonify(drone_controller.adjust_position(x, y))


# API для обновления высоты дрона
@app.route('/altitude', methods=['POST'])
def update_altitude():
    data = request.get_json()
    altitude = data.get('altitude', 0)
    return jsonify(drone_controller.adjust_altitude(altitude))


# API для обновления скорости дрона
@app.route('/speed', methods=['POST'])
def update_speed():
    data = request.get_json()
    speed = data.get('speed', 0)
    return jsonify(drone_controller.adjust_speed(speed))


# API для проверки заряда батареи
@app.route('/battery', methods=['GET'])
def check_battery():
    return jsonify(drone_controller.monitor_battery())


# API для симуляции препятствий
@app.route('/simulate_obstacle', methods=['GET'])
def simulate_obstacle():
    obstacle_distance = sensor_simulator.simulate_obstacle()
    if obstacle_distance < 10:
        return jsonify(
            drone_view.display_alert(f"Obstacle detected {obstacle_distance} meters away! Adjusting course..."))
    return jsonify({"obstacle_distance": obstacle_distance})


# API для симуляции погодных условий
@app.route('/simulate_weather', methods=['GET'])
def simulate_weather():
    weather = sensor_simulator.simulate_weather_conditions()
    return jsonify(weather)


if __name__ == '__main__':
    app.run(debug=True)
