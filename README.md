# NBA Team Explorer 🏀

An Angular application for browsing NBA teams and rosters. It demonstrates
component-based UI design, search, navigation, and shared data services.

## Contents

- [Introduction](#introduction)
- [How to Run](#how-to-run)
- [Architecture](#architecture)
- [Improvements](#improvements)
- [Conclusion](#conclusion)
- [Code Review](#code-review)

## Introduction

The interface combines a searchable team sidebar with a focused roster view.
TypeScript models and Angular services keep data access separate from display logic.

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

- **TeamService:** fetches team and player data.
- **TeamSidebarComponent:** handles navigation and search.
- **TeamDetailsComponent:** presents the selected team's roster.

## Improvements

- Keep search results synchronized through the sidebar input handler.
- Centralize roster state in the data service.
- Add RxJS error handling for failed API requests.

## Conclusion

The project is a compact example of Angular components, TypeScript models, and
service-driven state working together.
