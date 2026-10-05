import { TeamSidebar } from './team-sidebar';

describe('TeamSidebar', () => {
  it('shows every team when initialized', () => {
    const component = new TeamSidebar();

    component.ngOnInit();

    expect(component.filteredTeams).toEqual(component.teams);
  });

  it('filters teams case-insensitively from entered search text', () => {
    const component = new TeamSidebar();
    const query = component.teams[0].name.slice(0, 3).toLowerCase();

    component.onSearch({ target: { value: query.toUpperCase() } } as unknown as Event);

    expect(component.filteredTeams.length).toBeGreaterThan(0);
    expect(component.filteredTeams.every(team =>
      team.name.toLowerCase().includes(query),
    )).toBeTrue();
  });
});
