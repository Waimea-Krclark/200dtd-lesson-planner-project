# Sprint 3 - A Refined and Complete System


## Sprint Goals

Develop the system until it is fully featured, with a refined UI and it satisfies the requirements. The system will be fully tested at this point.


---

## Updated Database Schema (if it changed)

Replace this text with notes regarding the DB schema.

![SCREENSHOT OF DB SCHEMA](screenshots/example.png)


---

## Final Implementation

The web app is fully implemented with a refined UI:

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE SYSTEM HERE**


---

While Designing the website, I discovered a major bug that occured when deleting a lesson that has resources connected to it. The lesson gets deleted but the resource remains, keeping the ID of the lesson saved, so when the resource is interacted with, an error is thrown as the resource has an out of bounds lesson_id parameter. To solve this I made it also delete resources connected to that lesson when the lesson is deleted.

Showing this to my end-user, I got feedback saying that it would be better if the user had and option to delete or reassign, as the resources could still be used or needed by the user. To achieve this i set up a system that allows the conflicting resources to be reassigned to a new lesson or deleted, to prevent errors.

![New conflicts menu](screenshots/ResourceConflict.png)

---

## Resources lesson clarification

One of the things my end-user commented on was the lessons listing when creating or editing a resource. Currently it will just display all the options by name, and the user can select the lesson, however my end user said that there may be multiple of the same or similar lessons in a week and it should be clear which one is which.


![Old Lessons display](screenshots/ResourceLessons.png)
![Lessons with same name](screenshots/SameLessonsError.png)

### Changes / Improvements

To solve this, I made the lessons display what day they are as well, making it a lot more obvious which lesson is which. I showed this to my end user who agreed it looked better and was more clear for the user. Doing this introduced a bug, because the name of the lesson displaying wasn't exactly the same as the real lessons name in the database as it was also including the day. Since the way it is formated and the fact is uses the 3 character day code, I can remove the last 6 characters from the string ( - MON) which will return it back to the exact lesson name everytime so it can be checked with the database.

![New display showing day code as well](screenshots/UpdatedLessonResources.png)


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing FEATURE NAME HERE

Replace this text with notes about what you are testing, how you tested it, and the outcome of the testing

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Sprint Review

Replace this text with a statement about how the sprint has moved the project forward - key success point, any things that didn't go so well, etc.

