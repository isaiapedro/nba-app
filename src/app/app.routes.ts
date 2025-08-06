import { Routes } from '@angular/router';
import { PlayerPage } from './player-page/player-page';
import { Predictor } from './predictor/predictor';
import { TeamDetails } from './team-page/team-details';
import { PlayerDetails } from './player-page/player-details';
import { TeamSidebar } from './team-page/team-sidebar';

export const routes: Routes = [
    { path: "", redirectTo: "team-page", pathMatch: "full" },
    {
        path: 'team-page',
        component: TeamSidebar,
        children: [
            {
                path: '',
                component: TeamDetails
            },
            {
                path: ':id',
                component: TeamDetails,
            },
        ]
    },
    {
        path: 'player-page',
        component: PlayerPage,
    },
    {
        path: 'player-page/:id',
        component: PlayerDetails,
        outlet: "details",
    },
    {
        path: 'predictor',
        component: Predictor
    }
];
