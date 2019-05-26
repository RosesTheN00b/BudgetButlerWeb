import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SettingsComponent } from './settings.component';
import { LoginComponent } from '../auth/login/login.component';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { MobileComponent } from '../sidebar/mobile/mobile.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule, MatButtonModule, MatDatepickerModule, MatNativeDateModule, MatCardModule, MatFormFieldModule, MatIconModule, MatInputModule, MatSnackBarModule, MatChipsModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ALTES_PASSWORT_FEHLT, PASSWORT_ZU_KURZ, PASSWORT_IDENTISCH, PASSWOERTER_NICHT_GLEICH } from '../errormessages';
import { AdduserComponent } from './adduser/adduser.component';
import { RouterTestingModule } from '@angular/router/testing';

describe('SettingsComponent', () => {
  let component: SettingsComponent;
  let fixture: ComponentFixture<SettingsComponent>;

  const onePassword = '123456789';
  const tooShortPassword = '123';
  const anotherPassword = '123456789abc';

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        SettingsComponent,
        AdduserComponent
      ],
      imports: [
        HttpClientTestingModule,
        FormsModule,
        MatSelectModule,
        MatButtonModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatButtonModule,
        MatCardModule,
        MatFormFieldModule,
        MatIconModule,
        MatChipsModule,
        MatInputModule,
        MatSnackBarModule,
        ReactiveFormsModule,
        RouterTestingModule,
        BrowserAnimationsModule,
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should show error message when nothing given', () => {
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(ALTES_PASSWORT_FEHLT);
  });

  it('should show error message when no new pw given', () => {
    component.altesPasswort.setValue(onePassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(PASSWORT_ZU_KURZ);
  });

  it('should show error message when all pw are equal', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(onePassword);
    component.neuesPasswortWiederholung.setValue(onePassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(PASSWORT_IDENTISCH);
  });

  it('should show error message when new pw to short', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(tooShortPassword);
    component.neuesPasswortWiederholung.setValue(tooShortPassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(PASSWORT_ZU_KURZ);
  });

  it('should show error message when new pws are not equal', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(anotherPassword);
    component.neuesPasswortWiederholung.setValue(anotherPassword + 'wrong');
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual(PASSWOERTER_NICHT_GLEICH);
  });

  it('should show no error message when everything is ok', () => {
    component.altesPasswort.setValue(onePassword);
    component.neuesPasswort.setValue(anotherPassword);
    component.neuesPasswortWiederholung.setValue(anotherPassword);
    component.computeErrorMesage();
    expect(component.errorMessage).toEqual('');
  });

});