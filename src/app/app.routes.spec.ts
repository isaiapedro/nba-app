import { routes } from './app.routes';

describe('application routes', () => {
  it('redirects the root path to the team explorer', () => {
    const rootRoute = routes.find(route => route.path === '');

    expect(rootRoute?.redirectTo).toBe('team-page');
    expect(rootRoute?.pathMatch).toBe('full');
  });

  it('provides team, player, and predictor navigation surfaces', () => {
    expect(routes.map(route => route.path)).toEqual([
      '',
      'team-page',
      'player-page',
      'predictor',
    ]);
  });
});
