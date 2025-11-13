# PHP Web Development with Copilot: Building a RESTful Blog API

## Learning Objective
Learn how to use GitHub Copilot to develop modern PHP web applications, implementing RESTful APIs, database operations, authentication, and following MVC architecture patterns.

## Instructions
1. Create a PHP REST API for a blog system
2. Use Copilot to implement CRUD operations
3. Learn PHP best practices and security patterns
4. Implement JWT authentication
5. Add advanced features like search, pagination, and caching

## Prerequisites
- PHP 8.1 or later installed
- Composer for dependency management
- MySQL or PostgreSQL database
- Postman or similar API testing tool
- Visual Studio Code with GitHub Copilot

## Your Task

### Part 1: Project Setup

#### Step 1: Initialize Project
```bash
# Create project directory
mkdir blog-api
cd blog-api

# Initialize composer
composer init

# Install dependencies
composer require slim/slim:"4.*"
composer require slim/psr7
composer require firebase/php-jwt
composer require vlucas/phpdotenv
composer require illuminate/database
composer require respect/validation

# Install dev dependencies
composer require --dev phpunit/phpunit
composer require --dev squizlabs/php_codesniffer
```

#### Step 2: Project Structure
Create the following directory structure:

```
blog-api/
├── config/
│   ├── database.php
│   └── routes.php
├── src/
│   ├── Controllers/
│   ├── Models/
│   ├── Middleware/
│   ├── Services/
│   ├── Repositories/
│   └── Validators/
├── public/
│   └── index.php
├── tests/
├── .env.example
├── .gitignore
└── composer.json
```

#### Step 3: Environment Configuration
Create `.env.example`:

```env
# Ask Copilot: "Create environment configuration for PHP API"
DB_DRIVER=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=blog_api
DB_USERNAME=root
DB_PASSWORD=

JWT_SECRET=your-secret-key-change-this
JWT_EXPIRATION=3600

APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000

CACHE_ENABLED=true
CACHE_DRIVER=file
```

### Part 2: Database Setup

#### Step 1: Database Configuration
Create `config/database.php`:

```php
<?php
// Ask Copilot: "Create database configuration using Illuminate Database"
use Illuminate\Database\Capsule\Manager as Capsule;

$capsule = new Capsule;

$capsule->addConnection([
    'driver'    => $_ENV['DB_DRIVER'],
    'host'      => $_ENV['DB_HOST'],
    'port'      => $_ENV['DB_PORT'],
    'database'  => $_ENV['DB_DATABASE'],
    'username'  => $_ENV['DB_USERNAME'],
    'password'  => $_ENV['DB_PASSWORD'],
    'charset'   => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix'    => '',
]);

$capsule->setAsGlobal();
$capsule->bootEloquent();

return $capsule;
```

#### Step 2: Database Migrations
Create `migrations/001_create_users_table.php`:

```php
<?php
// Ask Copilot: "Create users table migration with password hashing"
use Illuminate\Database\Capsule\Manager as Capsule;

Capsule::schema()->create('users', function ($table) {
    $table->id();
    $table->string('username')->unique();
    $table->string('email')->unique();
    $table->string('password');
    $table->string('full_name');
    $table->text('bio')->nullable();
    $table->string('avatar_url')->nullable();
    $table->enum('role', ['admin', 'author', 'reader'])->default('reader');
    $table->boolean('is_active')->default(true);
    $table->timestamp('email_verified_at')->nullable();
    $table->timestamps();
    $table->softDeletes();

    // Let Copilot add indexes
});
```

Create `migrations/002_create_posts_table.php`:

```php
<?php
// Ask Copilot: "Create posts table migration with relationships"
use Illuminate\Database\Capsule\Manager as Capsule;

Capsule::schema()->create('posts', function ($table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->string('title');
    $table->string('slug')->unique();
    $table->text('content');
    $table->text('excerpt')->nullable();
    $table->string('featured_image')->nullable();
    $table->enum('status', ['draft', 'published', 'archived'])->default('draft');
    $table->timestamp('published_at')->nullable();
    $table->integer('view_count')->default(0);
    $table->timestamps();
    $table->softDeletes();

    // Let Copilot add full-text search index
});
```

Create `migrations/003_create_categories_and_tags.php`:

```php
<?php
// Ask Copilot: "Create categories and tags tables with pivot tables"
use Illuminate\Database\Capsule\Manager as Capsule;

// Let Copilot implement categories, tags, and many-to-many relationships
```

Create `migrations/004_create_comments_table.php`:

```php
<?php
// Ask Copilot: "Create comments table with nested comments support"
use Illuminate\Database\Capsule\Manager as Capsule;

// Let Copilot implement comments with parent-child relationships
```

### Part 3: Models

#### Step 1: User Model
Create `src/Models/User.php`:

```php
<?php
// Ask Copilot: "Create User model with Eloquent ORM"
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class User extends Model
{
    use SoftDeletes;

    protected $fillable = [
        'username',
        'email',
        'password',
        'full_name',
        'bio',
        'avatar_url',
        'role',
        'is_active'
    ];

    protected $hidden = [
        'password',
        'deleted_at'
    ];

    protected $casts = [
        'is_active' => 'boolean',
        'email_verified_at' => 'datetime',
        'created_at' => 'datetime',
        'updated_at' => 'datetime'
    ];

    // Relationships
    public function posts()
    {
        // Let Copilot implement relationship
    }

    public function comments()
    {
        // Let Copilot implement relationship
    }

    // Methods
    public function setPasswordAttribute($value)
    {
        // Let Copilot implement password hashing
    }

    public function verifyPassword($password)
    {
        // Let Copilot implement password verification
    }

    public function isAdmin()
    {
        // Let Copilot implement role check
    }

    // Let Copilot add JWT token generation method
}
```

#### Step 2: Post Model
Create `src/Models/Post.php`:

```php
<?php
// Ask Copilot: "Create Post model with relationships and scopes"
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use SoftDeletes;

    protected $fillable = [
        'user_id',
        'title',
        'slug',
        'content',
        'excerpt',
        'featured_image',
        'status',
        'published_at'
    ];

    protected $casts = [
        'published_at' => 'datetime',
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
        'view_count' => 'integer'
    ];

    // Relationships
    public function author()
    {
        // Let Copilot implement relationship
    }

    public function categories()
    {
        // Let Copilot implement many-to-many relationship
    }

    public function tags()
    {
        // Let Copilot implement many-to-many relationship
    }

    public function comments()
    {
        // Let Copilot implement relationship
    }

    // Scopes
    public function scopePublished($query)
    {
        // Let Copilot implement published scope
    }

    public function scopeByAuthor($query, $userId)
    {
        // Let Copilot implement author filter
    }

    public function scopeSearch($query, $term)
    {
        // Let Copilot implement full-text search
    }

    // Methods
    public function generateSlug()
    {
        // Let Copilot implement slug generation
    }

    public function incrementViewCount()
    {
        // Let Copilot implement view counter
    }

    // Let Copilot add more helper methods
}
```

### Part 4: Controllers

#### Step 1: Base Controller
Create `src/Controllers/BaseController.php`:

```php
<?php
// Ask Copilot: "Create base controller with JSON response helpers"
namespace App\Controllers;

use Psr\Http\Message\ResponseInterface as Response;

abstract class BaseController
{
    protected function jsonResponse(Response $response, $data, int $status = 200): Response
    {
        // Let Copilot implement JSON response formatting
    }

    protected function successResponse(Response $response, $data, string $message = 'Success'): Response
    {
        // Let Copilot implement success response
    }

    protected function errorResponse(Response $response, string $message, int $status = 400, $errors = null): Response
    {
        // Let Copilot implement error response
    }

    protected function paginatedResponse(Response $response, $data, int $page, int $perPage, int $total): Response
    {
        // Let Copilot implement paginated response
    }

    protected function getUserFromRequest($request)
    {
        // Let Copilot implement user extraction from JWT token
    }
}
```

#### Step 2: Auth Controller
Create `src/Controllers/AuthController.php`:

```php
<?php
// Ask Copilot: "Create authentication controller with JWT"
namespace App\Controllers;

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use App\Models\User;
use App\Services\JWTService;
use App\Validators\UserValidator;

class AuthController extends BaseController
{
    private $jwtService;

    public function __construct(JWTService $jwtService)
    {
        $this->jwtService = $jwtService;
    }

    public function register(Request $request, Response $response): Response
    {
        $data = $request->getParsedBody();

        // Let Copilot implement registration with validation
    }

    public function login(Request $request, Response $response): Response
    {
        $data = $request->getParsedBody();

        // Let Copilot implement login with JWT token generation
    }

    public function logout(Request $request, Response $response): Response
    {
        // Let Copilot implement logout (token invalidation)
    }

    public function refresh(Request $request, Response $response): Response
    {
        // Let Copilot implement token refresh
    }

    public function me(Request $request, Response $response): Response
    {
        // Let Copilot implement current user profile
    }

    public function updateProfile(Request $request, Response $response): Response
    {
        // Let Copilot implement profile update
    }

    public function changePassword(Request $request, Response $response): Response
    {
        // Let Copilot implement password change
    }
}
```

#### Step 3: Post Controller
Create `src/Controllers/PostController.php`:

```php
<?php
// Ask Copilot: "Create CRUD controller for posts with filtering and pagination"
namespace App\Controllers;

use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use App\Models\Post;
use App\Repositories\PostRepository;
use App\Validators\PostValidator;

class PostController extends BaseController
{
    private $postRepository;

    public function __construct(PostRepository $postRepository)
    {
        $this->postRepository = $postRepository;
    }

    public function index(Request $request, Response $response): Response
    {
        // Get query parameters
        $params = $request->getQueryParams();
        $page = $params['page'] ?? 1;
        $perPage = $params['per_page'] ?? 10;
        $status = $params['status'] ?? null;
        $search = $params['search'] ?? null;
        $category = $params['category'] ?? null;
        $tag = $params['tag'] ?? null;

        // Let Copilot implement filtering, searching, and pagination
    }

    public function show(Request $request, Response $response, array $args): Response
    {
        $slug = $args['slug'];

        // Let Copilot implement single post retrieval with view count
    }

    public function store(Request $request, Response $response): Response
    {
        $data = $request->getParsedBody();
        $user = $this->getUserFromRequest($request);

        // Let Copilot implement post creation with validation
    }

    public function update(Request $request, Response $response, array $args): Response
    {
        $id = $args['id'];
        $data = $request->getParsedBody();
        $user = $this->getUserFromRequest($request);

        // Let Copilot implement post update with authorization
    }

    public function destroy(Request $request, Response $response, array $args): Response
    {
        $id = $args['id'];
        $user = $this->getUserFromRequest($request);

        // Let Copilot implement post deletion with authorization
    }

    public function publish(Request $request, Response $response, array $args): Response
    {
        // Let Copilot implement post publishing
    }

    public function unpublish(Request $request, Response $response, array $args): Response
    {
        // Let Copilot implement post unpublishing
    }
}
```

### Part 5: Middleware

#### Step 1: JWT Authentication Middleware
Create `src/Middleware/AuthMiddleware.php`:

```php
<?php
// Ask Copilot: "Create JWT authentication middleware"
namespace App\Middleware;

use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Server\RequestHandlerInterface as RequestHandler;
use Slim\Psr7\Response;
use App\Services\JWTService;

class AuthMiddleware
{
    private $jwtService;

    public function __construct(JWTService $jwtService)
    {
        $this->jwtService = $jwtService;
    }

    public function __invoke(Request $request, RequestHandler $handler): Response
    {
        // Let Copilot implement JWT token verification
    }
}
```

#### Step 2: CORS Middleware
Create `src/Middleware/CorsMiddleware.php`:

```php
<?php
// Ask Copilot: "Create CORS middleware for API"
namespace App\Middleware;

use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Server\RequestHandlerInterface as RequestHandler;
use Slim\Psr7\Response;

class CorsMiddleware
{
    public function __invoke(Request $request, RequestHandler $handler): Response
    {
        // Let Copilot implement CORS headers
    }
}
```

#### Step 3: Rate Limiting Middleware
Create `src/Middleware/RateLimitMiddleware.php`:

```php
<?php
// Ask Copilot: "Create rate limiting middleware"
namespace App\Middleware;

use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Server\RequestHandlerInterface as RequestHandler;
use Slim\Psr7\Response;

class RateLimitMiddleware
{
    private $maxRequests;
    private $timeWindow;

    public function __construct(int $maxRequests = 60, int $timeWindow = 60)
    {
        $this->maxRequests = $maxRequests;
        $this->timeWindow = $timeWindow;
    }

    public function __invoke(Request $request, RequestHandler $handler): Response
    {
        // Let Copilot implement rate limiting logic
    }
}
```

### Part 6: Services

#### Step 1: JWT Service
Create `src/Services/JWTService.php`:

```php
<?php
// Ask Copilot: "Create JWT service for token generation and verification"
namespace App\Services;

use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use App\Models\User;

class JWTService
{
    private $secret;
    private $expiration;

    public function __construct()
    {
        $this->secret = $_ENV['JWT_SECRET'];
        $this->expiration = $_ENV['JWT_EXPIRATION'] ?? 3600;
    }

    public function generateToken(User $user): string
    {
        // Let Copilot implement token generation
    }

    public function verifyToken(string $token): ?object
    {
        // Let Copilot implement token verification
    }

    public function refreshToken(string $token): ?string
    {
        // Let Copilot implement token refresh
    }

    public function decodeToken(string $token): ?object
    {
        // Let Copilot implement token decoding
    }
}
```

#### Step 2: Cache Service
Create `src/Services/CacheService.php`:

```php
<?php
// Ask Copilot: "Create file-based cache service"
namespace App\Services;

class CacheService
{
    private $cacheDir;
    private $defaultTtl;

    public function __construct(string $cacheDir = './cache', int $defaultTtl = 3600)
    {
        $this->cacheDir = $cacheDir;
        $this->defaultTtl = $defaultTtl;

        if (!is_dir($cacheDir)) {
            mkdir($cacheDir, 0755, true);
        }
    }

    public function get(string $key, $default = null)
    {
        // Let Copilot implement cache retrieval
    }

    public function set(string $key, $value, ?int $ttl = null): bool
    {
        // Let Copilot implement cache storage
    }

    public function has(string $key): bool
    {
        // Let Copilot implement cache existence check
    }

    public function delete(string $key): bool
    {
        // Let Copilot implement cache deletion
    }

    public function clear(): bool
    {
        // Let Copilot implement cache clearing
    }

    private function getCacheFilePath(string $key): string
    {
        // Let Copilot implement file path generation
    }

    private function isExpired(array $cached): bool
    {
        // Let Copilot implement expiration check
    }
}
```

#### Step 3: Email Service
Create `src/Services/EmailService.php`:

```php
<?php
// Ask Copilot: "Create email service for notifications"
namespace App\Services;

class EmailService
{
    private $fromEmail;
    private $fromName;

    public function __construct()
    {
        $this->fromEmail = $_ENV['MAIL_FROM_ADDRESS'] ?? 'noreply@example.com';
        $this->fromName = $_ENV['MAIL_FROM_NAME'] ?? 'Blog API';
    }

    public function sendWelcomeEmail(string $to, string $username): bool
    {
        // Let Copilot implement welcome email
    }

    public function sendPasswordResetEmail(string $to, string $resetToken): bool
    {
        // Let Copilot implement password reset email
    }

    public function sendVerificationEmail(string $to, string $verificationToken): bool
    {
        // Let Copilot implement email verification
    }

    private function send(string $to, string $subject, string $body): bool
    {
        // Let Copilot implement email sending logic
    }
}
```

### Part 7: Repositories

#### Step 1: Post Repository
Create `src/Repositories/PostRepository.php`:

```php
<?php
// Ask Copilot: "Create repository pattern for post queries"
namespace App\Repositories;

use App\Models\Post;

class PostRepository
{
    public function findAll(array $filters = [], int $page = 1, int $perPage = 10)
    {
        // Let Copilot implement advanced filtering and pagination
    }

    public function findBySlug(string $slug): ?Post
    {
        // Let Copilot implement slug-based retrieval
    }

    public function findById(int $id): ?Post
    {
        // Let Copilot implement ID-based retrieval
    }

    public function create(array $data): Post
    {
        // Let Copilot implement creation logic
    }

    public function update(Post $post, array $data): bool
    {
        // Let Copilot implement update logic
    }

    public function delete(Post $post): bool
    {
        // Let Copilot implement soft delete
    }

    public function search(string $query, int $page = 1, int $perPage = 10)
    {
        // Let Copilot implement full-text search
    }

    public function getPopular(int $limit = 10)
    {
        // Let Copilot implement popular posts query
    }

    public function getRecent(int $limit = 10)
    {
        // Let Copilot implement recent posts query
    }

    public function getByCategory(int $categoryId, int $page = 1, int $perPage = 10)
    {
        // Let Copilot implement category filtering
    }

    public function getByTag(int $tagId, int $page = 1, int $perPage = 10)
    {
        // Let Copilot implement tag filtering
    }
}
```

### Part 8: Validators

#### Step 1: Post Validator
Create `src/Validators/PostValidator.php`:

```php
<?php
// Ask Copilot: "Create validation rules for posts using Respect Validation"
namespace App\Validators;

use Respect\Validation\Validator as v;

class PostValidator
{
    public static function validateCreate(array $data): array
    {
        $errors = [];

        // Let Copilot implement validation rules for post creation
        // Title, content, status, etc.

        return $errors;
    }

    public static function validateUpdate(array $data): array
    {
        // Let Copilot implement validation rules for post update
    }

    private static function validateTitle($title): ?string
    {
        // Let Copilot implement title validation
    }

    private static function validateContent($content): ?string
    {
        // Let Copilot implement content validation
    }

    private static function validateStatus($status): ?string
    {
        // Let Copilot implement status validation
    }
}
```

### Part 9: Routes Configuration

Create `config/routes.php`:

```php
<?php
// Ask Copilot: "Create RESTful API routes for blog application"
use Slim\App;
use App\Controllers\AuthController;
use App\Controllers\PostController;
use App\Controllers\CommentController;
use App\Controllers\CategoryController;
use App\Controllers\TagController;
use App\Middleware\AuthMiddleware;

return function (App $app) {
    // Public routes
    $app->group('/api', function ($group) {
        // Authentication
        $group->post('/auth/register', [AuthController::class, 'register']);
        $group->post('/auth/login', [AuthController::class, 'login']);

        // Public posts
        $group->get('/posts', [PostController::class, 'index']);
        $group->get('/posts/{slug}', [PostController::class, 'show']);

        // Categories and tags
        $group->get('/categories', [CategoryController::class, 'index']);
        $group->get('/tags', [TagController::class, 'index']);
    });

    // Protected routes
    $app->group('/api', function ($group) {
        // Auth user routes
        $group->get('/auth/me', [AuthController::class, 'me']);
        $group->post('/auth/logout', [AuthController::class, 'logout']);
        $group->put('/auth/profile', [AuthController::class, 'updateProfile']);
        $group->post('/auth/change-password', [AuthController::class, 'changePassword']);

        // Post management
        $group->post('/posts', [PostController::class, 'store']);
        $group->put('/posts/{id}', [PostController::class, 'update']);
        $group->delete('/posts/{id}', [PostController::class, 'destroy']);
        $group->post('/posts/{id}/publish', [PostController::class, 'publish']);

        // Let Copilot add more protected routes
    })->add(AuthMiddleware::class);
};
```

### Part 10: Application Bootstrap

Create `public/index.php`:

```php
<?php
// Ask Copilot: "Create Slim application bootstrap with middleware"
use Slim\Factory\AppFactory;
use DI\Container;
use Dotenv\Dotenv;

require __DIR__ . '/../vendor/autoload.php';

// Load environment variables
$dotenv = Dotenv::createImmutable(__DIR__ . '/..');
$dotenv->load();

// Initialize database
require __DIR__ . '/../config/database.php';

// Create container
$container = new Container();

// Set container to create App with on AppFactory
AppFactory::setContainer($container);
$app = AppFactory::create();

// Add error middleware
$app->addErrorMiddleware(
    $_ENV['APP_DEBUG'] === 'true',
    true,
    true
);

// Add body parsing middleware
$app->addBodyParsingMiddleware();

// Add routing middleware
$app->addRoutingMiddleware();

// Load routes
$routes = require __DIR__ . '/../config/routes.php';
$routes($app);

// Run application
$app->run();
```

## What You'll Learn
- Modern PHP development with Composer
- RESTful API design principles
- Slim Framework for routing and middleware
- Eloquent ORM for database operations
- JWT authentication implementation
- Repository pattern for data access
- Input validation and sanitization
- Error handling and logging
- API documentation
- Security best practices

## Success Criteria
- [ ] User registration and login work correctly
- [ ] JWT tokens are generated and validated
- [ ] CRUD operations for posts function properly
- [ ] Pagination and filtering work correctly
- [ ] Authentication middleware protects routes
- [ ] Validation prevents invalid data
- [ ] Database relationships work correctly
- [ ] API returns consistent JSON responses
- [ ] Error handling is comprehensive
- [ ] Code follows PSR standards

## Test Scenarios

### Authentication Tests
```bash
# Register new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'

# Get current user (with token)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Post Tests
```bash
# List posts with pagination
curl -X GET "http://localhost:8000/api/posts?page=1&per_page=10&status=published"

# Get single post
curl -X GET "http://localhost:8000/api/posts/my-first-post"

# Create post (authenticated)
curl -X POST http://localhost:8000/api/posts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content...",
    "status": "published",
    "categories": [1, 2],
    "tags": ["php", "tutorial"]
  }'

# Update post
curl -X PUT http://localhost:8000/api/posts/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content..."
  }'

# Delete post
curl -X DELETE http://localhost:8000/api/posts/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Advanced Challenges

### Challenge 1: Image Upload
Implement image upload for posts with resizing and CDN integration:

```php
// Ask Copilot: "Create image upload service with validation and resizing"
class ImageService
{
    public function upload($file, string $type = 'post'): array
    {
        // Validate, resize, and store image
    }
}
```

### Challenge 2: Full-Text Search
Implement advanced search with Elasticsearch or database full-text search:

```php
// Ask Copilot: "Implement full-text search for posts"
class SearchService
{
    public function search(string $query, array $filters = []): array
    {
        // Implement search with relevance scoring
    }
}
```

### Challenge 3: API Documentation
Add OpenAPI/Swagger documentation:

```php
// Ask Copilot: "Generate OpenAPI documentation for blog API"
```

### Challenge 4: WebSocket Notifications
Add real-time notifications using WebSockets:

```php
// Ask Copilot: "Implement WebSocket server for real-time notifications"
```

### Challenge 5: GraphQL Alternative
Create GraphQL endpoint alongside REST API:

```php
// Ask Copilot: "Add GraphQL support to blog API"
```

## Real-World Extensions
- Add Redis caching layer
- Implement background job processing
- Add API versioning
- Create admin dashboard
- Implement OAuth2 authentication
- Add monitoring and logging
- Create Docker containerization
- Set up CI/CD pipeline
- Add API rate limiting per user
- Implement API analytics

## Expected Learning Outcomes
By completing this exercise, you will understand:
- Modern PHP application architecture
- RESTful API design and implementation
- Authentication and authorization patterns
- Database design and ORM usage
- Input validation and security
- Middleware and request/response lifecycle
- Repository and service patterns
- Error handling and logging
- API testing and documentation
- PHP best practices and PSR standards
