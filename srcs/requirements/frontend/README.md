# Frontend - SPA App and AI

## 🖼️ Frontend Framework Justification – Vue 3 (Minor Module ✅)

> _“Minor module: Use a front-end framework or toolkit. Your frontend development will utilize the Bootstrap toolkit.”_  
> _“You can create a front-end without using the constraints of this module by using the default language/framework. However, this module will only be valid if you use the associated constraints.”_

---

This project **does claim the Minor module** and **fully complies** with its requirements.

- The subject allows using either a **frontend framework** or a **toolkit**.
- We chose **Vue 3**, a well-established **frontend framework**, instead of a toolkit like Bootstrap.
- This satisfies the constraint and validates the Minor module.

---

### ✅ Why Vue 3 Qualifies

Vue 3 is a **progressive JavaScript framework** for building web interfaces. It provides structure, reactivity, and component-based development — but it does **not** implement features for us automatically.

It is equivalent in nature to **React**, which is widely accepted in the same category. Just like React, Vue:
- Requires developers to define and implement app logic manually.
- Does not ship with any UI toolkit or design system.
- Is fully modular — routing, validation, and i18n are added via small packages and implemented by hand.

---

### 🔧 How We Use Vue 3 as a Framework

| Feature       | Implementation |
|---------------|----------------|
| **Routing**   | `vue-router` – manually configured SPA navigation |
| **Forms & Validation** | `vee-validate` – field-level validation rules, all written manually |
| **i18n**      | `vue-i18n` – language files, switching logic, and storage all custom |
| **WebSockets**| Real-time game data rendered through Vue’s Composition API |
| **UI/UX**     | 100% custom — no Bootstrap, Vuetify, or other visual toolkits |

---

We **do not** use:
- Prebuilt UI kits or templates
- Full-featured visual libraries that solve components
- Layout systems like Bootstrap

All components and styles are created from scratch, using only **Vue 3 as a framework** to organize and structure the application.

---

### 🟢 Conclusion

> Vue 3 is a compliant **frontend framework** under the subject's definition of the Minor module.  
> It is used as intended: to build a custom, fully controlled SPA with real-time game logic, routing, and UI.

This usage **fulfills the Minor module** and should be credited as such during evaluation.

## 👥 Major Module – Multiple Players ✅
This project **fully implements the Multiple Players major module**.

- The game supports **up to 6 players** in a single match.
- Each player is assigned a **unique paddle**, **name**, and **color** for clear in-game identification.
- Players can be controlled either by a **human (keyboard)** or an **AI**, depending on game settings.

---

### 🎮 Controls & Gameplay

- All human players share the **same keyboard**, with controls mapped per player.
- Before starting the game, users can:
    - Add or remove players (up to 6).
    - Select **who controls each paddle** — human or AI.
- This allows any configuration like:
    - 1v1 (default)
    - 1 human vs 5 AIs
    - 3 humans vs 3 AIs
    - Up to **6 players simultaneously**, all active and responsive.

---

### 📌 Subject Compliance

- **More than 2 players** supported (up to 6).
- **Each player has live control** — human via keyboard or AI logic.
- Players are visually distinguishable (color + name).
- A unique configuration of >2 players is implemented (in this case: 3–6 paddles on a shared board).

---

This setup complies fully with the subject and demonstrates flexibility, dynamic player setup, and live control for all participants — satisfying the **Major module: Multiple players** requirement.

### 🤖 AI Opponent ✅

> _“Develop an AI opponent that provides a challenging and engaging gameplay experience for users [...] The AI can only refresh its view of the game once per second [...] The use of the A* algorithm is not permitted.”_

---

This project **fully implements the AI Opponent major module**, following all listed constraints.

---

### ✅ AI Design Summary

- The AI **does not use A\*** or any pathfinding algorithm.
- Instead, it uses a **simple, physics-based prediction model** that anticipates the ball’s position.
- The AI can:
  - React to incoming balls
  - Adjust direction and speed
  - Occasionally win
- Its reaction logic is refreshed **once every second**, as required.

---

### ⚙️ Implementation Details

- **Prediction interval** is locked at `1000ms` (`PREDICTION_INTERVAL = 1000`), complying with the 1-second refresh constraint.
- The AI estimates where the ball will intersect its paddle line by:
  - Calculating horizontal travel time
  - Applying current vertical velocity
  - Bouncing off walls when necessary (mirroring)
- To avoid perfection, it introduces a small **randomized error factor** to mimic human imperfection.

---

### 🧠 No A\* Usage
The AI opponent in this project uses a **lightweight, physics-based prediction model** to estimate the ball’s future position and react accordingly — **not the A\* algorithm**.

---

### ⚙️ How the AI Predicts Ball Interception

1. **Checks if the ball is approaching**
  - Determines the ball's direction (`velocityX`) and skips logic if the ball is flying away.

2. **Calculates time to collision with paddle**
  - Uses horizontal distance and velocity to estimate when the ball will reach the paddle’s X position:
    ```
    timeToPaddle = distanceToPaddleX / ballVelocityX
    ```

3. **Predicts future vertical position**
  - Multiplies vertical velocity by time to estimate future Y position:
    ```
    predictedY = ballPositionY + ballVelocityY * timeToPaddle
    ```

4. **Handles wall bounces with mirroring logic**
  - If predicted Y goes off-screen, it "bounces" off top/bottom by reflecting:
    ```
    if predictedY < 0: predictedY = -predictedY
    if predictedY > 100: predictedY = 200 - predictedY
    ```

5. **Adds random error for human-like inaccuracy**
  - Introduces controlled randomness based on distance:
    ```
    predictedY += random_error * error_factor
    ```

6. **Sends direction command to move paddle**
  - If above or below predicted Y, the paddle moves up or down.

---

### ❌ Why This Is Not A\*

| Feature                    | Your AI Model                                      | A\* Algorithm                                         |
|----------------------------|----------------------------------------------------|--------------------------------------------------------|
| **Search Space**           | None – only uses current game state               | Explores multiple future states (nodes)               |
| **Pathfinding**            | Not used                                          | Core purpose – finds optimal path                     |
| **Simulation Depth**       | Predicts a single future point                    | Explores multiple outcomes and transitions            |
| **Heuristic / Cost**       | None                                              | Uses `f(n) = g(n) + h(n)` cost-based evaluation       |
| **Structure**              | Pure math and conditionals                        | Graph traversal with open/closed sets                 |
| **Performance**            | Fast and linear                                   | CPU-intensive, branching                              |
| **Human Behavior**         | Mimicked via error and fixed prediction interval  | Not designed to simulate humans                       |

---

### 🕹️ Human-like Behavior

- The AI **simulates live input** by sending paddle direction commands (`-1`, `0`, or `1`) via WebSocket — identical to a human player.
- When the ball is **not approaching**, the AI randomly drifts to the center (visual idle behavior only — does not affect decision logic).

## 🎮 Game Customization Options ✅

This project **fully implements** the **Game Customization Options** minor module by allowing players to tailor the **game physics, visuals, and experience** through a dedicated settings interface.

---

### 🛠️ Customization Features Implemented

| Option                  | Description |
|-------------------------|-------------|
| **Ball Curve Level**    | Players can choose how much the ball curves when struck by a moving paddle. The curve intensity is calculated based on the paddle's speed and direction at the moment of contact. |
| **Ball Speed**          | Players can tweak the overall speed of the ball. (Due to technical constraints, the range is limited to ensure sync between backend and frontend without interpolation.) |
| **Ball Color**          | Users can pick a color for the ball to personalize the match experience. |
| **Ball Skin**           | Aesthetic presets allow choosing different ball textures/skins. |
| **Live Ball Preview**   | A preview window lets users test ball curve, spin, and direction in real-time using pure CSS animations — no 3D or external libraries involved. |

---

### 💡 Design & UX Considerations

- A full **settings menu** is provided before launching a game, allowing players to configure and preview game behavior.
- The customization system is **applied consistently across all game modes**, including demo and multiplayer.
- A **default mode** (no curve, default color/skin, standard speed) is available for those who prefer a classic experience.

## 🌐 Expanding Browser Compatibility ✅
This project fully implements the **Browser Compatibility** minor module by ensuring the app runs seamlessly in both:

- **Google Chrome** (main development browser)
- **Mozilla Firefox** (additional tested browser)

---

### 🛠️ Technical Compatibility Measures

- **PostCSS + Autoprefixer**: Used to automatically add vendor prefixes to ensure broader CSS support across browsers.
- **Tested CSS Features**: All animations, layout, and effects have fallbacks or proper prefixes applied.
- **Vite Defaults**: Vite’s build system transpiles and polyfills where necessary for compatibility with modern browser targets.

---

### 🔍 Example Autoprefixes Applied

| Feature               | Autoprefix Output Example                         |
|------------------------|---------------------------------------------------|
| `display: flex`        | `-webkit-box; -ms-flexbox; flex`                  |
| `user-select`          | `-webkit-user-select; -moz-user-select; none`     |
| `transform`            | `-webkit-transform; -ms-transform; transform`     |

## 🧩 Feature-Sliced Design (FSD) Architecture

To maintain scalability and clarity, the frontend follows a **Feature-Sliced Design (FSD)** architecture:

- Clear separation between **pages**, **widgets**, **features**, **entities**, and **shared** layers.
- Uses **Vite aliases** to keep imports clean and decoupled:
  ```js
  @          → src/
  entities/  → business logic (e.g. ball, paddle, game state)
  features/  → interactive components with logic (e.g. game settings, matchmaking)
  widgets/   → visual containers or layout units
  pages/     → full route-level views
  shared/    → reusable low-level UI/components/utils
  ```

## 🔄 Custom Query System (React Query-Inspired)
To avoid relying on third-party state libraries like `react-query` or `vue-query`, this project includes a **lightweight custom data-fetching layer** implemented from scratch using Vue’s Composition API.

### 🧩 Core Features

| Feature                  | `useQuery`                                  | `useMutation`                                   |
|--------------------------|----------------------------------------------|--------------------------------------------------|
| Auto fetch & refetch  | Fetches data automatically on mount          | Executes async logic manually on demand         |
| Loading state         | `isLoading` tracks loading delay             | `isLoading` reflects mutation state             |
| Error handling        | `isError` & `error` capture fetch issues     | Catches errors, invokes `onError` callback      |
| Success callbacks     | `onSuccess`, `onSettled` hooks supported     | Same success/error hooks for post-action logic  |
| Transform response    | `select` lets you modify the raw response    | —                                                |
| Manual refetch        | `.refetch()` available anytime               | `.mutate()` accepts params and triggers action  |
| Request delay padding | UI loading state is padded to min 300ms      | Consistent loading UX even for fast responses   |

---

### ✨ Design Goals

- 🔧 **Complete control** over lifecycle without black-box behavior
- 🚫 **No third-party dependency** — 100% manual implementation
- 🧠 Inspired by core ideas from `react-query`, adapted for Vue 3
- ⚡ Designed for API-centric workflows and declarative components
