import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
 
import { AuthGuard } from './auth/auth.guard';
import { LoginComponent } from './auth/login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AddausgabeComponent } from './addausgabe/addausgabe.component';
import { AllebuchungenComponent } from './allebuchungen/allebuchungen.component';
import { SettingsComponent } from './settings/settings.component';
import { AddeinnahmeComponent } from './addeinnahme/addeinnahme.component';

 
const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { canActivate: [AuthGuard], path: '', children:
    [
      { path: 'dashboard', component: DashboardComponent},
      { path: 'addausgabe', component: AddausgabeComponent},
      { path: 'addeinnahme', component: AddeinnahmeComponent},
      { path: 'allebuchungen', component: AllebuchungenComponent},
      { path: 'settings', component: SettingsComponent},
      { path: '', component: AddausgabeComponent}
    ]},
];
 
@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}