import math
import time
from typing import Tuple, Optional
from pynput.mouse import Listener as MouseListener, Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key, GlobalHotKeys

class ShellShockAimbot:
    def __init__(self):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        
        self.player_pos: Optional[Tuple[int, int]] = None
        self.enemy_pos: Optional[Tuple[int, int]] = None
        
        self.optimal_shot: Optional[Tuple[int, int]] = None
        self.high_shot: Optional[Tuple[int, int]] = None

    def calc_velocity(self, dist_x: float, dist_y: float, angle: int) -> float:
        """Calculate the required velocity for a given distance and angle."""
        g = -379.106
        q = 0.0518718
        
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        tan_a = math.tan(angle_rad)
        
        try:
            val = (-g * dist_x * dist_x) / (2 * cos_a * cos_a * (tan_a * dist_x - dist_y))
            if val < 0:
                return float('inf')
            v0 = -2 / (g * q) * math.sqrt(val)
            return v0
        except (ValueError, ZeroDivisionError):
            return float('inf')

    def calculate_shots(self):
        """Calculate both optimal and high angle shots."""
        if not self.player_pos or not self.enemy_pos:
            return
            
        dist_x = abs(self.player_pos[0] - self.enemy_pos[0])
        dist_y = -(self.enemy_pos[1] - self.player_pos[1])
        
        smallest_velocity = float('inf')
        best_angle = 0
        
        # Calculate optimal shot (lowest velocity)
        for possible_angle in range(1, 90):
            v0 = self.calc_velocity(dist_x, dist_y, possible_angle)
            if v0 < smallest_velocity:
                smallest_velocity = v0
                best_angle = possible_angle
                
        if smallest_velocity != float('inf'):
            print(f"Optimal Shot -> Velocity: {smallest_velocity:.2f}, Angle: {best_angle}")
            self.optimal_shot = (round(smallest_velocity), best_angle)
            
        # Calculate highest shot below 100 power
        for possible_angle in range(1, 90):
            high_angle = 90 - possible_angle
            v0 = self.calc_velocity(dist_x, dist_y, high_angle)
            if v0 <= 100:
                print(f"High Shot -> Velocity: {v0:.2f}, Angle: {high_angle}")
                self.high_shot = (round(v0), high_angle)
                break

    def set_player_pos(self):
        print("Click your Tank")
        def on_click(x, y, button, pressed):
            if pressed:
                print(f"Player positioned at: {x}, {y}")
                self.player_pos = (x, y)
                self.calculate_shots()
                return False
                
        with MouseListener(on_click=on_click) as listener:
            listener.join()

    def set_enemy_pos(self):
        print("Click enemy Tank")
        def on_click(x, y, button, pressed):
            if pressed:
                print(f"Enemy positioned at: {x}, {y}")
                self.enemy_pos = (x, y)
                self.calculate_shots()
                return False
                
        with MouseListener(on_click=on_click) as listener:
            listener.join()

    def reset_to_100_90(self):
        """Resets the game UI to 100 power and 90 degrees."""
        if not self.player_pos:
            return
            
        px, py = self.player_pos
        self.mouse.position = (px, py)
        time.sleep(0.05)
        self.mouse.press(Button.left)
        time.sleep(0.05)
        # Move mouse to top of screen to max out power and set angle to 90
        self.mouse.position = (px, 0)
        time.sleep(0.05)
        self.mouse.release(Button.left)
        time.sleep(0.1)

    def apply_shot(self, target_power: int, target_angle: int):
        if not self.player_pos or not self.enemy_pos:
            print("Set both player and enemy positions first!")
            return
            
        self.reset_to_100_90()

        # Determine direction based on player relative to enemy
        direction = "right" if self.player_pos[0] < self.enemy_pos[0] else "left"
        
        diff_power = target_power - 100
        diff_angle = (target_angle - 90) if direction == "left" else (-target_angle + 90)
            
        # Apply power changes
        if diff_power > 0:
            for _ in range(diff_power):
                self.keyboard.tap(Key.up)
                time.sleep(0.02)
        else:
            for _ in range(-diff_power):
                self.keyboard.tap(Key.down)
                time.sleep(0.02)
                
        # Apply angle changes
        if diff_angle > 0:
            for _ in range(diff_angle):
                self.keyboard.tap(Key.right)
                time.sleep(0.02)
        else:
            for _ in range(-diff_angle):
                self.keyboard.tap(Key.left)
                time.sleep(0.02)
                
        # Clear positions after shot is prepared
        self.player_pos = None
        self.enemy_pos = None
        self.optimal_shot = None
        self.high_shot = None
        print("Ready for next target!")

    def prepare_optimal_shot(self):
        if self.optimal_shot:
            print(f"Preparing optimal shot: {self.optimal_shot}")
            self.apply_shot(*self.optimal_shot)
        else:
            print("Optimal shot not calculated yet.")

    def prepare_high_shot(self):
        if self.high_shot:
            print(f"Preparing high shot: {self.high_shot}")
            self.apply_shot(*self.high_shot)
        else:
            print("High shot not calculated yet.")

    def run(self):
        hotkeys = {
            '<ctrl>+<alt>+p': self.set_player_pos,
            '<ctrl>+<alt>+e': self.set_enemy_pos,
            '<ctrl>+<alt>+s': self.prepare_optimal_shot,
            '<ctrl>+<alt>+h': self.prepare_high_shot
        }
        
        print("=======================================")
        print("      ShellShockLive Aimbot Loaded     ")
        print("=======================================")
        print("Shortcuts:")
        print("  Ctrl+Alt+P : Set Player Position")
        print("  Ctrl+Alt+E : Set Enemy Position")
        print("  Ctrl+Alt+S : Prepare Optimal Shot")
        print("  Ctrl+Alt+H : Prepare High Angle Shot")
        print("=======================================")
        
        with GlobalHotKeys(hotkeys) as h:
            h.join()

if __name__ == "__main__":
    bot = ShellShockAimbot()
    bot.run()
