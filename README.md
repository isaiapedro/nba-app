# Angular Team App 🏀
### (Angular, TypeScript, HTML/CSS)

## Contents

- [Introduction](#introduction)
- [How to Run](#how-to-run)
- [Architecture](#architecture)
- [Improvements](#improvements)
- [Conclusion](#conclusion)
- [Code Review](#code-review)

## Introduction

This project is a basic Angular application designed to display team data. It features a team page component, a team sidebar component for navigation and searching, and a main application module structured with TypeScript.

## How to Run

1. Open the terminal or command prompt and navigate to the project directory
```bash
cd project-directory
```
2. Start the development server
```bash
ng serve
```
3. Open a web browser and navigate to the local server
```bash
http://localhost:4200
```
## Architecture

![Diagram](diagram.png)

• TeamService: An injectable service responsible for fetching team and player data from the backend API.

• TeamSidebarComponent: Handles the navigation sidebar, displaying a list of teams and managing the search filtering logic.

• TeamDetailsComponent: Displays the specific details and roster of the selected team.

## Improvements

To improve the current state of development, the following issues should be addressed:

• State Management: The filteredTeams property in the sidebar wasn't updating on search input changes. This was fixed by binding an onSearch event handler to the input.

• Memory Management: The players property in team-details.component.ts was initially assigned directly from a JSON array, which can lead to memory leaks upon frequent re-renders. A dedicated service now manages this state.

• Robustness: Implement error handling mechanisms using try-catch blocks or RxJS error handling operators to prevent the app from crashing on failed API calls.

## Conclusion

Thanks for reading up until here. I had a ton of fun doing this project and got a lot of useful insights on Angular components, TypeScript, and state management. If you want to see similar projects, go to my github page. Feel free to reach me on [LinkedIn](https://www.linkedin.com/in/isaiapedro/) or my [Webpage](https://isaiapedro.github.io/).

Bye! 👋
