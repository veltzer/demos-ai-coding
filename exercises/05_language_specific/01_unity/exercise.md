# Unity Game Development with Copilot: Building a 2D Platformer

## Learning Objective
Learn how to use GitHub Copilot to develop Unity games, understanding component-based architecture, game physics, input systems, UI design, and common game mechanics.

## Instructions
1. Create a new Unity 2D project
1. Use Copilot to implement a simple platformer game
1. Learn Unity-specific patterns and best practices
1. Implement player movement, enemies, collectibles, and UI
1. Add game state management and scene transitions

## Prerequisites
- Unity Hub installed (2022.3 LTS or later recommended)
- Visual Studio Code with Unity extension, or Visual Studio
- GitHub Copilot extension enabled
- Basic understanding of Unity Editor interface

## Your Task

### Part 1: Project Setup

#### Step 1: Create the Project
1. Open Unity Hub
1. Create new project -> 2D (Core) template
1. Name it "PlatformerGame"
1. Configure Visual Studio Code as external editor (Edit -> Preferences -> External Tools)

#### Step 2: Setup Project Structure
Create the following folder structure in Assets:

```txt
Assets/
+-- Scripts/
|   +-- Player/
|   +-- Enemies/
|   +-- Collectibles/
|   +-- Managers/
|   +-- UI/
+-- Prefabs/
+-- Sprites/
+-- Animations/
+-- Scenes/
+-- Audio/
```

### Part 2: Player Controller

#### Step 1: Basic Player Movement
Create `Scripts/Player/PlayerController.cs`:

```csharp
// Ask Copilot: "Create a 2D platformer player controller with smooth movement"
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [Header("Movement Settings")]
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float jumpForce = 10f;
    [SerializeField] private float acceleration = 10f;
    [SerializeField] private float deceleration = 10f;

    [Header("Ground Check")]
    [SerializeField] private Transform groundCheck;
    [SerializeField] private float groundCheckRadius = 0.2f;
    [SerializeField] private LayerMask groundLayer;

    [Header("Jump Settings")]
    [SerializeField] private float coyoteTime = 0.2f;
    [SerializeField] private float jumpBufferTime = 0.2f;

    private Rigidbody2D rb;
    private bool isGrounded;
    private float coyoteTimeCounter;
    private float jumpBufferCounter;
    private float horizontalInput;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        // Let Copilot implement initialization
    }

    private void Update()
    {
        // Handle input
        horizontalInput = Input.GetAxisRaw("Horizontal");

        // Let Copilot implement jump input with buffer and coyote time
    }

    private void FixedUpdate()
    {
        // Let Copilot implement smooth movement physics
    }

    private void CheckGrounded()
    {
        // Let Copilot implement ground detection
    }

    private void Jump()
    {
        // Let Copilot implement jump mechanics
    }

    // Let Copilot add wall jump, double jump, or dash mechanics
}
```

#### Step 2: Player Animation
Create `Scripts/Player/PlayerAnimator.cs`:

```csharp
// Ask Copilot: "Create player animation controller for 2D platformer"
using UnityEngine;

public class PlayerAnimator : MonoBehaviour
{
    [SerializeField] private Animator animator;
    [SerializeField] private SpriteRenderer spriteRenderer;

    private PlayerController playerController;
    private Rigidbody2D rb;

    // Animation parameter names
    private static readonly int Speed = Animator.StringToHash("Speed");
    private static readonly int IsGrounded = Animator.StringToHash("IsGrounded");
    private static readonly int VerticalVelocity = Animator.StringToHash("VerticalVelocity");
    private static readonly int Jump = Animator.StringToHash("Jump");

    private void Awake()
    {
        // Let Copilot implement initialization
    }

    private void Update()
    {
        // Let Copilot implement animation state updates
    }

    private void FlipSprite(float horizontalInput)
    {
        // Let Copilot implement sprite flipping
    }

    public void TriggerJumpAnimation()
    {
        // Let Copilot implement jump trigger
    }
}
```

#### Step 3: Player Health System
Create `Scripts/Player/PlayerHealth.cs`:

```csharp
// Ask Copilot: "Create a player health system with damage, healing, and death"
using UnityEngine;
using UnityEngine.Events;

public class PlayerHealth : MonoBehaviour
{
    [Header("Health Settings")]
    [SerializeField] private int maxHealth = 100;
    [SerializeField] private int currentHealth;

    [Header("Invincibility")]
    [SerializeField] private float invincibilityDuration = 1.5f;
    [SerializeField] private float flashInterval = 0.1f;

    [Header("Events")]
    public UnityEvent<int, int> OnHealthChanged; // current, max
    public UnityEvent OnDeath;
    public UnityEvent OnDamageTaken;
    public UnityEvent OnHealed;

    private bool isInvincible;
    private SpriteRenderer spriteRenderer;

    private void Awake()
    {
        currentHealth = maxHealth;
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    public void TakeDamage(int damage)
    {
        if (isInvincible) return;

        // Let Copilot implement damage logic with invincibility
    }

    public void Heal(int amount)
    {
        // Let Copilot implement healing logic
    }

    private IEnumerator InvincibilityCoroutine()
    {
        // Let Copilot implement invincibility with visual feedback
    }

    private void Die()
    {
        // Let Copilot implement death logic
    }

    // Let Copilot add respawn functionality
}
```

### Part 3: Enemy System

#### Step 1: Base Enemy Class
Create `Scripts/Enemies/Enemy.cs`:

```csharp
// Ask Copilot: "Create a base enemy class for 2D platformer"
using UnityEngine;

public abstract class Enemy : MonoBehaviour
{
    [Header("Enemy Stats")]
    [SerializeField] protected int maxHealth = 50;
    [SerializeField] protected int currentHealth;
    [SerializeField] protected int damage = 10;
    [SerializeField] protected float moveSpeed = 2f;

    [Header("Detection")]
    [SerializeField] protected float detectionRange = 5f;
    [SerializeField] protected LayerMask playerLayer;

    [Header("Drops")]
    [SerializeField] protected GameObject[] dropItems;
    [SerializeField] protected int scoreValue = 100;

    protected Transform player;
    protected Rigidbody2D rb;
    protected bool isDead;

    protected virtual void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        currentHealth = maxHealth;
        player = GameObject.FindGameObjectWithTag("Player")?.transform;
    }

    protected virtual void Update()
    {
        if (isDead) return;
        // Let Copilot implement base update logic
    }

    public virtual void TakeDamage(int damage)
    {
        // Let Copilot implement damage logic
    }

    protected virtual void Die()
    {
        // Let Copilot implement death, drops, and score
    }

    protected abstract void Move();
    protected abstract void Attack();

    protected bool IsPlayerInRange()
    {
        // Let Copilot implement player detection
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        // Let Copilot implement collision damage to player
    }
}
```

#### Step 2: Patrolling Enemy
Create `Scripts/Enemies/PatrolEnemy.cs`:

```csharp
// Ask Copilot: "Create a patrolling enemy for 2D platformer"
using UnityEngine;

public class PatrolEnemy : Enemy
{
    [Header("Patrol Settings")]
    [SerializeField] private Transform[] waypoints;
    [SerializeField] private float waypointReachDistance = 0.1f;
    [SerializeField] private float pauseDuration = 1f;

    private int currentWaypointIndex;
    private bool isPaused;
    private SpriteRenderer spriteRenderer;

    protected override void Awake()
    {
        base.Awake();
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    protected override void Move()
    {
        if (isPaused || waypoints.Length == 0) return;

        // Let Copilot implement patrol movement logic
    }

    protected override void Attack()
    {
        // Patrol enemies don't actively attack, damage on collision
    }

    private IEnumerator PauseAtWaypoint()
    {
        // Let Copilot implement pause logic
    }
}
```

#### Step 3: Flying Enemy
Create `Scripts/Enemies/FlyingEnemy.cs`:

```csharp
// Ask Copilot: "Create a flying enemy that follows the player"
using UnityEngine;

public class FlyingEnemy : Enemy
{
    [Header("Flying Settings")]
    [SerializeField] private float followSpeed = 3f;
    [SerializeField] private float minDistanceToPlayer = 2f;
    [SerializeField] private float verticalOffset = 1f;
    [SerializeField] private float smoothing = 2f;

    [Header("Attack Settings")]
    [SerializeField] private GameObject projectilePrefab;
    [SerializeField] private Transform firePoint;
    [SerializeField] private float attackCooldown = 2f;

    private float lastAttackTime;

    protected override void Move()
    {
        if (player == null || !IsPlayerInRange()) return;

        // Let Copilot implement smooth following behavior
    }

    protected override void Attack()
    {
        if (Time.time < lastAttackTime + attackCooldown) return;

        // Let Copilot implement projectile shooting
    }
}
```

### Part 4: Collectibles and Power-ups

#### Step 1: Collectible Base Class
Create `Scripts/Collectibles/Collectible.cs`:

```csharp
// Ask Copilot: "Create a base collectible class with different types"
using UnityEngine;

public abstract class Collectible : MonoBehaviour
{
    [SerializeField] protected int value = 1;
    [SerializeField] protected AudioClip collectSound;
    [SerializeField] protected GameObject collectEffect;
    [SerializeField] protected float rotationSpeed = 100f;
    [SerializeField] protected float bobSpeed = 2f;
    [SerializeField] protected float bobHeight = 0.2f;

    private Vector3 startPosition;

    protected virtual void Start()
    {
        startPosition = transform.position;
    }

    protected virtual void Update()
    {
        // Let Copilot implement floating and rotating animation
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            Collect(collision.gameObject);
        }
    }

    protected abstract void Collect(GameObject player);

    protected void PlayCollectEffects()
    {
        // Let Copilot implement visual and audio effects
    }
}
```

#### Step 2: Specific Collectibles
Create `Scripts/Collectibles/Coin.cs`:

```csharp
// Ask Copilot: "Create a coin collectible that adds score"
public class Coin : Collectible
{
    protected override void Collect(GameObject player)
    {
        // Let Copilot implement coin collection
        GameManager.Instance.AddScore(value);
        PlayCollectEffects();
        Destroy(gameObject);
    }
}
```

Create `Scripts/Collectibles/HealthPickup.cs`:

```csharp
// Ask Copilot: "Create a health pickup collectible"
public class HealthPickup : Collectible
{
    [SerializeField] private int healAmount = 25;

    protected override void Collect(GameObject player)
    {
        // Let Copilot implement health restoration
        var health = player.GetComponent<PlayerHealth>();
        if (health != null)
        {
            health.Heal(healAmount);
            PlayCollectEffects();
            Destroy(gameObject);
        }
    }
}
```

Create `Scripts/Collectibles/PowerUp.cs`:

```csharp
// Ask Copilot: "Create a power-up collectible with duration"
public class PowerUp : Collectible
{
    public enum PowerUpType
    {
        SpeedBoost,
        JumpBoost,
        Invincibility,
        DoubleJump
    }

    [SerializeField] private PowerUpType powerUpType;
    [SerializeField] private float duration = 10f;

    protected override void Collect(GameObject player)
    {
        // Let Copilot implement power-up application
    }
}
```

### Part 5: Game Manager

#### Step 1: Singleton Game Manager
Create `Scripts/Managers/GameManager.cs`:

```csharp
// Ask Copilot: "Create a singleton GameManager for 2D platformer"
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.Events;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    [Header("Game State")]
    [SerializeField] private int currentScore;
    [SerializeField] private int currentLives = 3;
    [SerializeField] private int currentLevel = 1;

    [Header("Events")]
    public UnityEvent<int> OnScoreChanged;
    public UnityEvent<int> OnLivesChanged;
    public UnityEvent OnGameOver;
    public UnityEvent OnLevelComplete;

    [Header("Settings")]
    [SerializeField] private bool isPaused;

    private void Awake()
    {
        // Let Copilot implement singleton pattern
    }

    public void AddScore(int points)
    {
        // Let Copilot implement score management
    }

    public void LoseLife()
    {
        // Let Copilot implement life system
    }

    public void PauseGame()
    {
        // Let Copilot implement pause functionality
    }

    public void ResumeGame()
    {
        // Let Copilot implement resume functionality
    }

    public void RestartLevel()
    {
        // Let Copilot implement level restart
    }

    public void LoadNextLevel()
    {
        // Let Copilot implement level progression
    }

    public void GameOver()
    {
        // Let Copilot implement game over logic
    }

    public void ReturnToMainMenu()
    {
        // Let Copilot implement menu navigation
    }

    // Let Copilot add save/load functionality
}
```

#### Step 2: Audio Manager
Create `Scripts/Managers/AudioManager.cs`:

```csharp
// Ask Copilot: "Create an audio manager for music and sound effects"
using UnityEngine;
using System.Collections.Generic;

public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance { get; private set; }

    [System.Serializable]
    public class Sound
    {
        public string name;
        public AudioClip clip;
        [Range(0f, 1f)] public float volume = 1f;
        [Range(0.1f, 3f)] public float pitch = 1f;
        public bool loop;
        [HideInInspector] public AudioSource source;
    }

    [SerializeField] private Sound[] sounds;
    [SerializeField] private AudioSource musicSource;

    private Dictionary<string, Sound> soundDictionary;

    private void Awake()
    {
        // Let Copilot implement singleton and initialization
    }

    public void PlaySound(string soundName)
    {
        // Let Copilot implement sound playback
    }

    public void PlayMusic(string musicName)
    {
        // Let Copilot implement music playback with crossfade
    }

    public void SetMusicVolume(float volume)
    {
        // Let Copilot implement volume control
    }

    public void SetSFXVolume(float volume)
    {
        // Let Copilot implement volume control
    }

    // Let Copilot add more audio management features
}
```

### Part 6: UI System

#### Step 1: HUD
Create `Scripts/UI/HUDManager.cs`:

```csharp
// Ask Copilot: "Create a HUD manager for health, score, and lives display"
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class HUDManager : MonoBehaviour
{
    [Header("Health Bar")]
    [SerializeField] private Slider healthSlider;
    [SerializeField] private Image healthFill;
    [SerializeField] private Gradient healthGradient;

    [Header("Score Display")]
    [SerializeField] private TextMeshProUGUI scoreText;
    [SerializeField] private Animator scoreAnimator;

    [Header("Lives Display")]
    [SerializeField] private GameObject[] lifeIcons;

    [Header("Power-Up Display")]
    [SerializeField] private GameObject powerUpPanel;
    [SerializeField] private Image powerUpIcon;
    [SerializeField] private TextMeshProUGUI powerUpTimerText;

    private void Start()
    {
        // Let Copilot implement event subscriptions
    }

    public void UpdateHealth(int currentHealth, int maxHealth)
    {
        // Let Copilot implement health bar update with smooth animation
    }

    public void UpdateScore(int score)
    {
        // Let Copilot implement score display with animation
    }

    public void UpdateLives(int lives)
    {
        // Let Copilot implement lives display
    }

    public void ShowPowerUp(Sprite icon, float duration)
    {
        // Let Copilot implement power-up indicator
    }

    // Let Copilot add combo system or other UI elements
}
```

#### Step 2: Pause Menu
Create `Scripts/UI/PauseMenu.cs`:

```csharp
// Ask Copilot: "Create a pause menu with resume, restart, and quit options"
using UnityEngine;
using UnityEngine.UI;

public class PauseMenu : MonoBehaviour
{
    [SerializeField] private GameObject pauseMenuUI;
    [SerializeField] private Button resumeButton;
    [SerializeField] private Button restartButton;
    [SerializeField] private Button settingsButton;
    [SerializeField] private Button quitButton;

    [SerializeField] private Slider musicVolumeSlider;
    [SerializeField] private Slider sfxVolumeSlider;

    private bool isPaused;

    private void Start()
    {
        // Let Copilot implement button event binding
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            if (isPaused) Resume();
            else Pause();
        }
    }

    public void Resume()
    {
        // Let Copilot implement resume logic
    }

    public void Pause()
    {
        // Let Copilot implement pause logic
    }

    public void Restart()
    {
        // Let Copilot implement restart logic
    }

    public void QuitToMainMenu()
    {
        // Let Copilot implement quit logic
    }
}
```

#### Step 3: Game Over Screen
Create `Scripts/UI/GameOverScreen.cs`:

```csharp
// Ask Copilot: "Create a game over screen with final score and options"
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class GameOverScreen : MonoBehaviour
{
    [SerializeField] private GameObject gameOverPanel;
    [SerializeField] private TextMeshProUGUI finalScoreText;
    [SerializeField] private TextMeshProUGUI highScoreText;
    [SerializeField] private Button retryButton;
    [SerializeField] private Button mainMenuButton;

    [SerializeField] private float fadeInDuration = 1f;
    [SerializeField] private CanvasGroup canvasGroup;

    private void Start()
    {
        gameOverPanel.SetActive(false);
        // Let Copilot implement initialization
    }

    public void ShowGameOver(int finalScore)
    {
        // Let Copilot implement game over display with animation
    }

    private IEnumerator FadeIn()
    {
        // Let Copilot implement fade-in animation
    }

    public void Retry()
    {
        // Let Copilot implement retry logic
    }

    public void ReturnToMainMenu()
    {
        // Let Copilot implement return to menu
    }
}
```

### Part 7: Advanced Features

#### Feature 1: Camera Controller
Create `Scripts/CameraController.cs`:

```csharp
// Ask Copilot: "Create a smooth camera follow with look-ahead"
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private float smoothSpeed = 0.125f;
    [SerializeField] private Vector3 offset = new Vector3(0, 0, -10);

    [Header("Look Ahead")]
    [SerializeField] private bool useLookAhead = true;
    [SerializeField] private float lookAheadDistance = 2f;
    [SerializeField] private float lookAheadSpeed = 2f;

    [Header("Bounds")]
    [SerializeField] private bool useBounds = true;
    [SerializeField] private Vector2 minBounds;
    [SerializeField] private Vector2 maxBounds;

    [Header("Camera Shake")]
    [SerializeField] private float shakeAmount = 0.1f;
    [SerializeField] private float shakeDecay = 1f;

    private float currentShakeAmount;
    private Vector3 currentVelocity;

    private void LateUpdate()
    {
        // Let Copilot implement smooth camera follow with look-ahead
    }

    public void Shake(float intensity, float duration)
    {
        // Let Copilot implement camera shake
    }

    private Vector3 ClampToBounds(Vector3 position)
    {
        // Let Copilot implement bounds clamping
    }
}
```

#### Feature 2: Checkpoint System
Create `Scripts/Checkpoint.cs`:

```csharp
// Ask Copilot: "Create a checkpoint system with visual feedback"
using UnityEngine;

public class Checkpoint : MonoBehaviour
{
    [SerializeField] private Sprite inactiveSprite;
    [SerializeField] private Sprite activeSprite;
    [SerializeField] private ParticleSystem activationEffect;
    [SerializeField] private AudioClip activationSound;

    private bool isActivated;
    private SpriteRenderer spriteRenderer;

    private void Awake()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player") && !isActivated)
        {
            ActivateCheckpoint();
        }
    }

    private void ActivateCheckpoint()
    {
        // Let Copilot implement checkpoint activation
    }
}
```

#### Feature 3: Object Pooling
Create `Scripts/ObjectPool.cs`:

```csharp
// Ask Copilot: "Create an object pooling system for performance"
using UnityEngine;
using System.Collections.Generic;

public class ObjectPool : MonoBehaviour
{
    [System.Serializable]
    public class Pool
    {
        public string tag;
        public GameObject prefab;
        public int size;
    }

    public static ObjectPool Instance { get; private set; }

    [SerializeField] private List<Pool> pools;
    private Dictionary<string, Queue<GameObject>> poolDictionary;

    private void Awake()
    {
        // Let Copilot implement singleton and pool initialization
    }

    public GameObject SpawnFromPool(string tag, Vector3 position, Quaternion rotation)
    {
        // Let Copilot implement object spawning from pool
    }

    public void ReturnToPool(string tag, GameObject obj)
    {
        // Let Copilot implement object return to pool
    }
}
```

## What You'll Learn
- Unity component-based architecture
- 2D physics and collision detection
- Input handling and player controls
- Animation state machines
- UI system and canvas
- Game state management
- Audio implementation
- Performance optimization (object pooling)
- Scene management
- Particle effects

## Success Criteria
- [ ] Player moves smoothly with jump mechanics
- [ ] Enemies patrol and chase player
- [ ] Collectibles work and update UI
- [ ] Health system with visual feedback
- [ ] Score and lives system functional
- [ ] Pause menu works correctly
- [ ] Game over screen displays properly
- [ ] Audio plays for actions and music
- [ ] Camera follows player smoothly
- [ ] Checkpoints save progress

## Advanced Challenges

### Challenge 1: Boss Battle
Create a multi-phase boss enemy with attack patterns

### Challenge 2: Level Editor
Create an in-game level editor with save/load functionality

### Challenge 3: Achievements
Implement an achievement system with unlockables

### Challenge 4: Mobile Controls
Add touch controls for mobile deployment

## Real-World Extensions
- Add more levels with increasing difficulty
- Implement a level selection screen
- Create different biomes/themes
- Add particle effects for polish
- Implement save system with PlayerPrefs
- Add leaderboard integration
- Create tutorials and onboarding

## Expected Learning Outcomes
By completing this exercise, you will understand:
- Unity game development workflow
- Component-based game architecture
- 2D game mechanics implementation
- UI/UX design for games
- Game state management patterns
- Performance optimization techniques
- Audio integration in games
- Physics-based gameplay
