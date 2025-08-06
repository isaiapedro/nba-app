import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import jsonData from '../data/active_players.json';
import jsonData2 from '../data/teams.json';
import { Player } from '../player';
import { Team } from '../team';

@Component({
  selector: 'app-team-details',
  //imports: [RouterLink, RouterOutlet],
  template: ``,
  styles: [
  ],
})

export class PlayerDetails {

  players: Player[] = jsonData.players;

  teams: Team[] = jsonData2.teams;

}
