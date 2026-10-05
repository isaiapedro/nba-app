import { PlayerPage } from './player-page';

describe('PlayerPage', () => {
  it('filters players case-insensitively from entered search text', () => {
    const component = new PlayerPage();
    const query = component.players[1].name.slice(0, 3).toLowerCase();

    component.onSearch({ target: { value: query.toUpperCase() } } as unknown as Event);

    expect(component.hasQuery).toBeTrue();
    expect(component.filteredPlayers.length).toBeGreaterThan(0);
    expect(component.filteredPlayers.every(player =>
      player.name.toLowerCase().includes(query),
    )).toBeTrue();
  });

  it('clears results when the search text is empty', () => {
    const component = new PlayerPage();

    component.onSearch({ target: { value: '' } } as unknown as Event);

    expect(component.hasQuery).toBeFalse();
    expect(component.filteredPlayers).toEqual([]);
  });
});
