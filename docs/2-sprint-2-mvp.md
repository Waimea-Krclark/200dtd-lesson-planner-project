# Sprint 2 - A Minimum Viable Product (MVP)


## Sprint Goals

Develop a bare-bones, working web application that provides the key functionality of the system, then test and refine it so that it can serve as the basis for the final phase of development in Sprint 3.


---

## Implemented Database Schema

Replace this text with notes regarding the DB schema.

![SCREENSHOT OF DB SCHEMA](screenshots/example.png)


---

## Initial Implementation

The key functionality of the web app was implemented:

![Home Page](screenshots/OldMVPHome.png)
![Day Page](<screenshots/Old Dropdown.png>)

---

## Testing Dropdown menus on for days

My initial dropdown menu system used the lesson id to find the dropdown that should be active to display the content, this meant that only one dropdown could be open at a time, and the page had to be reloaded each time. This made for a slow, inefficient system and my end user agreed that it needed improvement.

![Old Gif showing dropdown](screenshots/OldDrowdownDemo.gif)

### Changes / Improvements

I made it so that multiple dropdowns could be opened and closed at the same time but it was still slow as it required the page to be reloaded each time. My end user thought that being able to view multiple dropdowns increased efficiency a lot but it still was slow and bad to use.

I completely changed the way I was doing dropdowns, instead replacing it with a javascript file that uses the lesson id and classes to find and change the states of whatever dropdown was clicked, this allowed for instant use of the dropdowns, as well as having as many open as needed at any time. My end user said that this was a much better system that increased the functionality and useability of my application by a lot.

![New dropdown system](screenshots/NewDropdown.gif)


---

## Testing Time displaying for lessons

My end user noticed that initially the lesson times were displaying poorly and in 24hr time, and didnt order correctly. It made the times harder to read at a glance and it was difficult to understand what time lessons were actually set for.

![Old time display](<screenshots/Old Time.png>)

### Changes / Improvements

I replaced the way that time was inputted, using pico css inbuilt time for forms, this returned a string that would display in 24 hours and order correctly as it was formatted automatically.

![Improved Time Display](screenshots/ImprovedOldTime.png)

When I showed this fix to my end user, I got more feedback saying that for readability, the time should be in 12hr time instead. I made use of the time and date formatting script provided to format this time into a 12 hour readable format that was not confusing.

![Code for displaying time](<screenshots/Time Display.png>)

![Final Time Display](screenshots/FixedTime.png)
---

## Testing Resource displaying for lesson

If no resources, doesnt tell user, coul be confisign

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing Editing Resource

Resources aren't set in stone sp editing them = yes

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Testing opening resource links

no open in new page = bad

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE TESTING HERE**

### Changes / Improvements

Replace this text with notes any improvements you made as a result of the testing.

**PLACE SCREENSHOTS AND/OR ANIMATED GIFS OF THE IMPROVED SYSTEM HERE**


---

## Sprint Review

Replace this text with a statement about how the sprint has moved the project forward - key success point, any things that didn't go so well, etc.

