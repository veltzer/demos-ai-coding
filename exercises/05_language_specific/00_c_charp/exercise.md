# C# Development with Copilot: Building a Task Management System

## Learning Objective
Learn how to use GitHub Copilot to develop modern C# applications, leveraging language features like LINQ, async/await, dependency injection, and object-oriented design patterns.

## Instructions
1. Create a new C# console application
1. Use Copilot to implement a task management system
1. Learn C# best practices and modern patterns
1. Implement CRUD operations with file persistence
1. Add advanced features like search, filtering, and scheduling

## Prerequisites
- .NET 8.0 SDK or later installed
- Visual Studio Code or Visual Studio
- GitHub Copilot extension enabled

## Your Task

### Part 1: Project Setup

#### Step 1: Create the Project
```bash
# Create a new console application
dotnet new console -n TaskManager
cd TaskManager

# Add necessary packages
dotnet add package Newtonsoft.Json
dotnet add package System.CommandLine
```

#### Step 2: Define the Domain Models
Create `Models/Task.cs`:

```csharp
// Ask Copilot: "Create a Task model class with properties for task management"
namespace TaskManager.Models
{
    public class TaskItem
    {
        public Guid Id { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public TaskPriority Priority { get; set; }
        public TaskStatus Status { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? DueDate { get; set; }
        public DateTime? CompletedAt { get; set; }
        public List<string> Tags { get; set; }

        // Let Copilot add constructor and methods
    }

    public enum TaskPriority
    {
        Low,
        Medium,
        High,
        Critical
    }

    public enum TaskStatus
    {
        Todo,
        InProgress,
        Completed,
        Cancelled
    }
}
```

### Part 2: Repository Pattern

#### Step 1: Define the Interface
Create `Repositories/ITaskRepository.cs`:

```csharp
// Ask Copilot: "Create a repository interface for task management"
namespace TaskManager.Repositories
{
    public interface ITaskRepository
    {
        Task<IEnumerable<TaskItem>> GetAllAsync();
        Task<TaskItem?> GetByIdAsync(Guid id);
        Task<TaskItem> AddAsync(TaskItem task);
        Task<bool> UpdateAsync(TaskItem task);
        Task<bool> DeleteAsync(Guid id);
        Task<IEnumerable<TaskItem>> SearchAsync(string query);
        Task<IEnumerable<TaskItem>> GetByStatusAsync(TaskStatus status);
        Task<IEnumerable<TaskItem>> GetByPriorityAsync(TaskPriority priority);
        Task SaveChangesAsync();
        // Let Copilot suggest additional methods
    }
}
```

#### Step 2: Implement File-Based Repository
Create `Repositories/JsonTaskRepository.cs`:

```csharp
// Ask Copilot: "Implement a JSON file-based task repository with async operations"
using Newtonsoft.Json;

namespace TaskManager.Repositories
{
    public class JsonTaskRepository : ITaskRepository
    {
        private readonly string _filePath;
        private List<TaskItem> _tasks;
        private readonly SemaphoreSlim _semaphore = new(1, 1);

        public JsonTaskRepository(string filePath = "tasks.json")
        {
            _filePath = filePath;
            // Let Copilot implement initialization logic
        }

        private async Task LoadTasksAsync()
        {
            // Let Copilot implement async file loading with error handling
        }

        public async Task<IEnumerable<TaskItem>> GetAllAsync()
        {
            // Let Copilot implement with proper async patterns
        }

        public async Task<TaskItem?> GetByIdAsync(Guid id)
        {
            // Let Copilot implement LINQ query
        }

        // Let Copilot implement remaining methods
    }
}
```

### Part 3: Business Logic Layer

#### Step 1: Create Service Interface
Create `Services/ITaskService.cs`:

```csharp
// Ask Copilot: "Create a service interface for task business logic"
namespace TaskManager.Services
{
    public interface ITaskService
    {
        Task<TaskItem> CreateTaskAsync(string title, string description,
                                       TaskPriority priority, DateTime? dueDate);
        Task<bool> CompleteTaskAsync(Guid id);
        Task<bool> UpdateTaskStatusAsync(Guid id, TaskStatus status);
        Task<IEnumerable<TaskItem>> GetOverdueTasksAsync();
        Task<IEnumerable<TaskItem>> GetTasksDueTodayAsync();
        Task<IEnumerable<TaskItem>> GetTasksByTagAsync(string tag);
        Task<Dictionary<TaskStatus, int>> GetTaskStatisticsAsync();
        // Let Copilot suggest more business methods
    }
}
```

#### Step 2: Implement Task Service
Create `Services/TaskService.cs`:

```csharp
// Ask Copilot: "Implement task service with validation and business rules"
namespace TaskManager.Services
{
    public class TaskService : ITaskService
    {
        private readonly ITaskRepository _repository;

        public TaskService(ITaskRepository repository)
        {
            _repository = repository;
        }

        public async Task<TaskItem> CreateTaskAsync(string title, string description,
                                                    TaskPriority priority, DateTime? dueDate)
        {
            // Validation
            if (string.IsNullOrWhiteSpace(title))
                throw new ArgumentException("Title cannot be empty", nameof(title));

            // Let Copilot implement creation logic
        }

        public async Task<IEnumerable<TaskItem>> GetOverdueTasksAsync()
        {
            var tasks = await _repository.GetAllAsync();
            // Let Copilot implement LINQ query for overdue tasks
        }

        public async Task<Dictionary<TaskStatus, int>> GetTaskStatisticsAsync()
        {
            var tasks = await _repository.GetAllAsync();
            // Let Copilot implement LINQ grouping and counting
        }

        // Let Copilot implement remaining methods
    }
}
```

### Part 4: Command Line Interface

#### Step 1: Setup Command Line Parser
Update `Program.cs`:

```csharp
// Ask Copilot: "Create a CLI app using System.CommandLine for task management"
using System.CommandLine;
using TaskManager.Models;
using TaskManager.Services;
using TaskManager.Repositories;

var rootCommand = new RootCommand("Task Management System");

// Add command
var addCommand = new Command("add", "Add a new task");
var titleOption = new Option<string>(
    "--title",
    "Task title") { IsRequired = true };
var descriptionOption = new Option<string>(
    "--description",
    "Task description");
var priorityOption = new Option<TaskPriority>(
    "--priority",
    () => TaskPriority.Medium,
    "Task priority");
var dueDateOption = new Option<DateTime?>(
    "--due",
    "Due date");

addCommand.AddOption(titleOption);
addCommand.AddOption(descriptionOption);
addCommand.AddOption(priorityOption);
addCommand.AddOption(dueDateOption);

addCommand.SetHandler(async (title, description, priority, dueDate) =>
{
    // Let Copilot implement add command handler
}, titleOption, descriptionOption, priorityOption, dueDateOption);

// List command
var listCommand = new Command("list", "List all tasks");
// Let Copilot implement list command with formatting

// Complete command
var completeCommand = new Command("complete", "Mark a task as completed");
// Let Copilot implement complete command

// Let Copilot add more commands (update, delete, search, stats)

rootCommand.AddCommand(addCommand);
rootCommand.AddCommand(listCommand);
rootCommand.AddCommand(completeCommand);

return await rootCommand.InvokeAsync(args);
```

### Part 5: Advanced Features

#### Feature 1: Task Filtering with LINQ
Create `Extensions/TaskExtensions.cs`:

```csharp
// Ask Copilot: "Create extension methods for advanced task filtering"
namespace TaskManager.Extensions
{
    public static class TaskExtensions
    {
        public static IEnumerable<TaskItem> FilterByDateRange(
            this IEnumerable<TaskItem> tasks,
            DateTime start,
            DateTime end)
        {
            // Let Copilot implement LINQ filtering
        }

        public static IEnumerable<TaskItem> SortByPriorityThenDueDate(
            this IEnumerable<TaskItem> tasks)
        {
            // Let Copilot implement complex sorting
        }

        public static IEnumerable<TaskItem> WithTags(
            this IEnumerable<TaskItem> tasks,
            params string[] tags)
        {
            // Let Copilot implement tag filtering
        }

        public static string ToFormattedString(this TaskItem task)
        {
            // Let Copilot implement pretty printing
        }

        // Let Copilot suggest more useful extensions
    }
}
```

#### Feature 2: Task Scheduling with Recurring Tasks
Create `Models/RecurringTask.cs`:

```csharp
// Ask Copilot: "Create a recurring task model with schedule patterns"
namespace TaskManager.Models
{
    public class RecurringTask
    {
        public Guid Id { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public RecurrencePattern Pattern { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public List<DateTime> Occurrences { get; set; }

        // Let Copilot implement methods to generate next occurrences
    }

    public enum RecurrencePattern
    {
        Daily,
        Weekly,
        Monthly,
        Yearly
    }
}
```

#### Feature 3: Notifications and Reminders
Create `Services/NotificationService.cs`:

```csharp
// Ask Copilot: "Create a notification service for task reminders"
namespace TaskManager.Services
{
    public interface INotificationService
    {
        Task SendReminderAsync(TaskItem task);
        Task CheckDueTasksAsync();
    }

    public class NotificationService : INotificationService
    {
        private readonly ITaskService _taskService;

        public NotificationService(ITaskService taskService)
        {
            _taskService = taskService;
        }

        public async Task CheckDueTasksAsync()
        {
            // Get tasks due soon
            var dueTasks = await _taskService.GetTasksDueTodayAsync();

            // Let Copilot implement notification logic
        }

        // Let Copilot implement reminder methods
    }
}
```

#### Feature 4: Export to Multiple Formats
Create `Services/ExportService.cs`:

```csharp
// Ask Copilot: "Create an export service supporting JSON, CSV, and Markdown"
namespace TaskManager.Services
{
    public class ExportService
    {
        private readonly ITaskRepository _repository;

        public ExportService(ITaskRepository repository)
        {
            _repository = repository;
        }

        public async Task ExportToCsvAsync(string filePath)
        {
            // Let Copilot implement CSV export
        }

        public async Task ExportToMarkdownAsync(string filePath)
        {
            // Let Copilot implement Markdown export
        }

        public async Task ExportToHtmlAsync(string filePath)
        {
            // Let Copilot implement HTML export with styling
        }

        // Let Copilot add import functionality
    }
}
```

### Part 6: Dependency Injection Setup

Create `DependencyInjection.cs`:

```csharp
// Ask Copilot: "Setup dependency injection for the task management system"
using Microsoft.Extensions.DependencyInjection;

namespace TaskManager
{
    public static class DependencyInjection
    {
        public static IServiceProvider ConfigureServices()
        {
            var services = new ServiceCollection();

            // Register repositories
            services.AddSingleton<ITaskRepository, JsonTaskRepository>();

            // Register services
            services.AddScoped<ITaskService, TaskService>();
            services.AddScoped<INotificationService, NotificationService>();
            services.AddScoped<ExportService>();

            return services.BuildServiceProvider();
        }
    }
}
```

## What You'll Learn
- Modern C# language features (LINQ, async/await, pattern matching)
- Repository pattern implementation
- Dependency injection principles
- Command-line application development
- File I/O with JSON serialization
- Extension methods and fluent APIs
- Error handling and validation
- SOLID principles in practice

## Success Criteria
- [ ] Can create tasks from command line
- [ ] Can list tasks with filtering options
- [ ] Tasks persist between application runs
- [ ] Can mark tasks as complete
- [ ] Can search and filter tasks
- [ ] Task statistics are calculated correctly
- [ ] Export functionality works for all formats
- [ ] Code follows C# naming conventions
- [ ] Async/await is used properly throughout

## Test Scenarios

### Basic Operations
```bash
# Add tasks
dotnet run -- add --title "Write documentation" --priority High --due 2024-12-31
dotnet run -- add --title "Code review" --priority Medium
dotnet run -- add --title "Team meeting" --priority Low --due 2024-12-20

# List all tasks
dotnet run -- list

# List by status
dotnet run -- list --status Todo

# List by priority
dotnet run -- list --priority High

# Complete a task
dotnet run -- complete --id <task-id>

# Search tasks
dotnet run -- search "documentation"

# Show statistics
dotnet run -- stats

# Export tasks
dotnet run -- export --format csv --output tasks.csv
```

## Advanced Challenges

### Challenge 1: Task Dependencies
Implement task dependencies where tasks can't be completed until their dependencies are done:

```csharp
// Ask Copilot: "Add task dependency tracking with validation"
public class TaskItem
{
    public List<Guid> DependsOn { get; set; }

    public bool CanComplete()
    {
        // Check if all dependencies are completed
    }
}
```

### Challenge 2: Task Templates
Create reusable task templates:

```csharp
// Ask Copilot: "Create a task template system with placeholders"
public class TaskTemplate
{
    public string Name { get; set; }
    public string TitleTemplate { get; set; }
    public string DescriptionTemplate { get; set; }
    public TaskPriority DefaultPriority { get; set; }

    public TaskItem CreateFromTemplate(Dictionary<string, string> variables)
    {
        // Replace placeholders with actual values
    }
}
```

### Challenge 3: Time Tracking
Add time tracking to tasks:

```csharp
// Ask Copilot: "Implement time tracking for tasks"
public class TaskTimeEntry
{
    public Guid Id { get; set; }
    public Guid TaskId { get; set; }
    public DateTime StartTime { get; set; }
    public DateTime? EndTime { get; set; }
    public TimeSpan Duration => EndTime.HasValue
        ? EndTime.Value - StartTime
        : TimeSpan.Zero;
    public string Notes { get; set; }
}
```

### Challenge 4: Task Collaboration
Add user assignment and collaboration features:

```csharp
// Ask Copilot: "Add user assignment and task collaboration features"
public class TaskAssignment
{
    public Guid TaskId { get; set; }
    public string AssignedTo { get; set; }
    public DateTime AssignedAt { get; set; }
    public string AssignedBy { get; set; }
}

public class TaskComment
{
    public Guid Id { get; set; }
    public Guid TaskId { get; set; }
    public string Author { get; set; }
    public string Content { get; set; }
    public DateTime CreatedAt { get; set; }
}
```

## Code Quality Improvements

### Unit Testing
Create `TaskManager.Tests/TaskServiceTests.cs`:

```csharp
// Ask Copilot: "Create unit tests for TaskService using xUnit and Moq"
using Xunit;
using Moq;
using TaskManager.Services;
using TaskManager.Repositories;

public class TaskServiceTests
{
    [Fact]
    public async Task CreateTaskAsync_WithValidData_ReturnsTask()
    {
        // Arrange
        var mockRepository = new Mock<ITaskRepository>();
        var service = new TaskService(mockRepository.Object);

        // Act & Assert
        // Let Copilot implement test
    }

    [Fact]
    public async Task CreateTaskAsync_WithEmptyTitle_ThrowsArgumentException()
    {
        // Let Copilot implement validation test
    }

    // Let Copilot generate more tests
}
```

### Logging
Add logging throughout the application:

```csharp
// Ask Copilot: "Add logging to the task service"
using Microsoft.Extensions.Logging;

public class TaskService : ITaskService
{
    private readonly ITaskRepository _repository;
    private readonly ILogger<TaskService> _logger;

    public TaskService(ITaskRepository repository, ILogger<TaskService> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public async Task<TaskItem> CreateTaskAsync(...)
    {
        _logger.LogInformation("Creating new task: {Title}", title);
        // Implementation with logging
    }
}
```

## Real-World Extensions
- Web API version using ASP.NET Core
- Blazor WebAssembly UI
- Database support with Entity Framework Core
- SignalR for real-time updates
- OAuth authentication
- Docker containerization

## Expected Learning Outcomes
By completing this exercise, you will understand:
- C# best practices and conventions
- Async programming patterns
- Repository and service patterns
- Dependency injection
- LINQ for data manipulation
- Command-line application architecture
- File persistence strategies
- Extension methods and fluent APIs
- Error handling and validation in C#
