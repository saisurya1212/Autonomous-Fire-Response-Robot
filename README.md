# 🤖 Autonomous Fire Response Robot

An intelligent **fire detection and response simulation** built using Python and Pygame. The system demonstrates how a **Model-Based Reflex Agent** can perceive its environment, remember the current state, navigate around obstacles, detect fires, extinguish them, and return to its base for charging.

## 🔥 Project Overview

The Autonomous Fire Response Robot simulates a robot operating in a grid-based environment where fires can occur at different locations.

The robot uses environmental information and its internal state to decide what action to take. When one or more fires are detected, the robot autonomously selects a fire, calculates a path while avoiding obstacles, moves toward the fire, extinguishes it, and continues responding to remaining fires.

After all fires are extinguished, the robot returns to its base and enters charging mode.

## 🧠 Why Model-Based Reflex Agent?

This project demonstrates a **Model-Based Reflex Agent** because the robot maintains an internal representation of its environment and uses the current state to make decisions.

The agent considers:

* Current robot position
* Fire locations
* Obstacles
* Battery level
* Current operating mode
* Previously detected environmental conditions

Based on this internal state, the robot selects an appropriate action such as:

**Detect → Navigate → Extinguish → Search for Next Fire → Return → Charge**

## 🚨 Key Features

* 🔥 Multiple fire detection
* 🤖 Autonomous robot navigation
* 🧠 Model-Based Reflex Agent architecture
* 🗺️ Grid-based environment
* 🚧 Obstacle avoidance
* 🔎 Fire detection using sensors
* 🧭 BFS pathfinding for navigation
* 💧 Fire extinguishing animation
* 🔋 Battery monitoring and charging
* 🏠 Automatic return to base
* 🎯 Sequential handling of multiple fires
* 📊 Real-time robot and fire status display
* 🎮 Interactive Pygame simulation

## Project Demo

![Autonomous Fire Detection & Response Robot](./fire-detection-robot-demo.png)

## 🛠️ Technologies Used

* **Python**
* **Pygame**
* **Breadth-First Search (BFS)**
* **Object-Oriented Programming**
* **Model-Based Reflex Agent concepts**

## 📁 Project Structure

```text
Autonomous-Fire-Response-Robot/
│
├── main.py          # Main simulation and agent control
├── robot.py         # Robot behavior and rendering
├── fire.py          # Fire behavior and extinguishing animation
├── sensor.py        # Environmental perception
├── settings.py      # Screen, grid and color configuration
├── assets/          # Robot and fire visual assets
└── README.md        # Project documentation
```

## ⚙️ How It Works

### 1. Environment

The simulation contains a grid representing the environment. Some cells contain obstacles that the robot cannot pass through.

### 2. Fire Detection

A fire can be placed at an available grid location. Multiple fires can exist simultaneously.

### 3. Decision Making

The robot evaluates the active fires and selects an appropriate target.

### 4. Pathfinding

The robot uses **Breadth-First Search (BFS)** to calculate a path while avoiding obstacles.

### 5. Fire Extinguishing

When the robot reaches the selected fire, it activates the extinguishing process.

### 6. Multiple Fire Handling

After extinguishing one fire, the robot checks for remaining active fires and automatically moves toward the next target.

### 7. Return to Base

When all fires have been extinguished, the robot calculates a path back to the base.

### 8. Charging

At the base, the robot enters charging mode and restores its battery.

## 🔄 Agent Workflow

```text
        Environment
             ↓
        Sensor Perception
             ↓
      Internal State / Model
             ↓
       Decision Making
             ↓
       Select Fire Target
             ↓
        BFS Pathfinding
             ↓
        Move to Fire
             ↓
       Extinguish Fire
             ↓
     More Fires Available?
        ↙            ↘
      YES             NO
       ↓               ↓
  Next Fire          Return
       ↓               ↓
  Extinguish        Charging
                       ↓
                Mission Complete
```

## ▶️ Installation

Make sure Python is installed on your system.

Install Pygame:

```bash
pip install pygame
```

## 🚀 Run the Project

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Autonomous-Fire-Response-Robot.git
```

Move into the project directory:

```bash
cd Autonomous-Fire-Response-Robot
```

Run the simulation:

```bash
python main.py
```

## 🎮 Controls

* **Mouse Click** → Place a fire on an available grid cell
* **ESC** → Exit the simulation

## 🎯 Project Objective

The main objective of this project is to demonstrate the practical working of a **Model-Based Reflex Agent** in an autonomous emergency-response scenario.

The simulation combines artificial intelligence concepts with pathfinding, environment perception, decision-making, and autonomous action.

## 🔮 Future Enhancements

* 🚁 Real-time camera-based fire detection
* 🌡️ Temperature and smoke sensors
* 🗺️ Dynamic environment mapping
* 🚗 Real robotic hardware integration
* 📡 IoT-based monitoring
* 🤖 Advanced AI-based fire detection
* 🧭 More advanced path planning algorithms
* 📱 Remote monitoring dashboard

## 👨‍💻 Project

**Autonomous Fire Response Robot**

Built as an educational AI project demonstrating **Model-Based Reflex Agents** using Python and Pygame.
