# Database ERD

## ER Diagram

```mermaid
erDiagram
    User {
        String id PK
        String email UK
        String password_hash
        String role
        String nim
        String program_studi
        String semester
        String name
        String interest
        String avatar_url
        DateTime created_at
        String mentor_id FK
    }

    Category {
        String id PK
        String name UK
        String slug UK
        String description
    }

    Course {
        String id PK
        String category_id FK
        String mentor_id FK
        String title
        Text description
        String level
        String status
        DateTime created_at
    }

    Module {
        String id PK
        String course_id FK
        String title
        Text description
        Integer order
        DateTime deadline
        DateTime created_at
    }

    Lesson {
        String id PK
        String module_id FK
        String title
        Text description
        Text content
        String lesson_type
        Integer order
        Integer duration
        DateTime created_at
        Boolean is_completed
        String task_code
    }

    Enrollment {
        String id PK
        String user_id FK
        String course_id FK
        Float progress_percentage
        Integer completed_lessons
        Integer total_lessons
        String status
        DateTime enrolled_at
    }

    LessonProgress {
        String id PK
        String user_id FK
        String lesson_id FK
        Boolean is_completed
        DateTime completed_at
        Text answers
        Float score
    }

    Quiz {
        String id PK
        String course_id FK
        String module_id FK
        String title
        Text description
        Integer time_limit
        Float passing_score
        Integer total_questions
        Boolean is_final
        DateTime created_at
    }

    Question {
        String id PK
        String quiz_id FK
        Text question_text
        String question_type
        Integer order
        Integer points
    }

    Option {
        String id PK
        String question_id FK
        Text option_text
        Boolean is_correct
        Integer order
    }

    QuizAttempt {
        String id PK
        String quiz_id FK
        String user_id FK
        Float score
        Float total_points
        Float percentage
        Boolean passed
        DateTime submitted_at
    }

    Assignment {
        String id PK
        String course_id FK
        String module_id FK
        String title
        Text description
        Text instructions
        DateTime due_date
        Float max_score
        JSON accepted_types
        DateTime created_at
    }

    Submission {
        String id PK
        String assignment_id FK
        String user_id FK
        String submission_type
        String file_url
        String github_url
        String url
        Text notes
        String status
        Float score
        Text feedback
        DateTime submitted_at
        DateTime graded_at
    }

    Announcement {
        String id PK
        String title
        Text description
        DateTime event_date
        String target_audience
        String mentor_id FK
        DateTime created_at
        String status
        DateTime scheduled_at
    }

    AnnouncementNotification {
        String id PK
        String announcement_id FK
        String user_id FK
        Boolean is_notified
        DateTime created_at
    }

    Project {
        String id PK
        String mentor_id FK
        String title
        Text description
        String whatsapp_link
        String github_link
        String image_url
        DateTime created_at
        DateTime updated_at
    }

    User ||--o{ Course : "mentors"
    User ||--o{ Enrollment : "has"
    User ||--o{ LessonProgress : "tracks"
    User ||--o{ QuizAttempt : "attempts"
    User ||--o{ Submission : "submits"
    User ||--o{ User : "mentors_member"
    User ||--o{ Announcement : "creates"
    User ||--o{ AnnouncementNotification : "receives"
    User ||--o{ Project : "creates"
    
    Category ||--o{ Course : "contains"
    
    Course ||--o{ Module : "contains"
    Course ||--o{ Enrollment : "has"
    Course ||--o{ Quiz : "has"
    Course ||--o{ Assignment : "has"
    
    Module ||--o{ Lesson : "contains"
    Module ||--o{ Quiz : "contains"
    Module ||--o{ Assignment : "contains"
    
    Lesson ||--o{ LessonProgress : "tracked_in"
    
    Quiz ||--o{ Question : "has"
    Quiz ||--o{ QuizAttempt : "has"
    
    Question ||--o{ Option : "has"
    
    Assignment ||--o{ Submission : "has"

    Announcement ||--o{ AnnouncementNotification : "triggers"
```

## Entities

- **User**: Represents a user in the system (member, mentor, admin). Contains authentication credentials and profile information, and optional `mentor_id` for mentor assignments.
- **Category**: Represents a classification grouping for courses.
- **Course**: The main entity for a learning subject. Authored by a mentor (User) and belongs to a Category.
- **Module**: A structural grouping unit within a Course. Contains lessons, quizzes, and assignments.
- **Lesson**: A specific teaching material (video, text, task) inside a Module.
- **Enrollment**: Tracks a User's participation in a Course, including their overall completion progress percentage.
- **LessonProgress**: Tracks a specific User's completion status and score for a specific Lesson.
- **Quiz**: A set of questions associated with a Module or Course.
- **Question**: A single question within a Quiz.
- **Option**: A multiple-choice answer option for a Question. Indicates if it is the correct answer.
- **QuizAttempt**: Tracks a User's attempt on a Quiz, containing their total score and pass/fail status.
- **Assignment**: A task given to students that requires manual submission. Belongs to a Module/Course.
- **Submission**: A User's submitted work for an Assignment, graded by a mentor.
- **Announcement**: General or specific announcements created by mentors/admins.
- **AnnouncementNotification**: Tracks whether a user has been notified or read a specific announcement.
- **Project**: Represents a project associated with a mentor's group. Mentors can post links (GitHub, WhatsApp), descriptions, and an image for their group.

## Relationships

- **1:N (User -> Course)**: A User (Mentor) can create many Courses.
- **1:N (Category -> Course)**: A Category can contain many Courses.
- **1:N (Course -> Module)**: A Course contains multiple Modules.
- **1:N (Module -> Lesson)**: A Module contains multiple Lessons.
- **1:N (Course -> Enrollment)**: A Course can have many enrolled Users.
- **1:N (User -> Enrollment)**: A User can enroll in many Courses.
- **1:N (Lesson -> LessonProgress)**: A Lesson has many progress records (one per user).
- **1:N (User -> LessonProgress)**: A User has many lesson progress records.
- **1:N (Course/Module -> Quiz/Assignment)**: Quizzes and Assignments belong to a Module (and Course).
- **1:N (Quiz -> Question)**: A Quiz has many Questions.
- **1:N (Question -> Option)**: A Question has many Options.
- **1:N (Quiz -> QuizAttempt)**: A Quiz can have many attempts.
- **1:N (Assignment -> Submission)**: An Assignment can have many submissions.
- **1:N (User -> Submission/QuizAttempt)**: A User can submit many assignments and attempt many quizzes.
- **1:N (User -> User)**: A User (Mentor) can mentor many other Users.
- **1:N (User -> Announcement)**: A User (Mentor/Admin) can create many announcements.
- **1:N (Announcement -> AnnouncementNotification)**: An announcement triggers many notifications.
- **1:N (User -> AnnouncementNotification)**: A User receives many notifications.
- **1:N (User -> Project)**: A User (Mentor) can create many group projects.

## Design Issues

1. **Redundant Foreign Keys (`course_id` and `module_id` on `Quiz` & `Assignment`)**
   Both `Quiz` and `Assignment` have foreign keys to `course_id` and `module_id`. Since a `Module` inherently belongs to a `Course`, maintaining a direct `course_id` link on the Quiz/Assignment table is technically a redundancy (denormalization). If a module were moved to a different course, the `course_id` on the related quizzes and assignments could become out of sync.
2. **Global state for `Lesson.is_completed`**
   The `Lesson` table contains an `is_completed` boolean field. Since lessons are shared among all enrolled users, this global state is conceptually incorrect (as noted in the model's source code comments). Real progress tracking should strictly rely on the `LessonProgress` table, making `Lesson.is_completed` redundant and a potential source of logic bugs if accidentally used.
3. **No unique constraint on progress/enrollment entities**
   The `Enrollment`, `LessonProgress`, and `QuizAttempt` models use surrogate primary keys (`id`), but there are no explicit unique constraints on their composite foreign keys. For example, a `User` should ideally only have one `Enrollment` per `Course`, or one `LessonProgress` per `Lesson`, but the database schema allows for duplicate rows.
