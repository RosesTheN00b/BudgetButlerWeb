import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MobileComponent } from './mobile.component';
import { MatIconModule, MatSnackBarModule } from '@angular/material';
import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('MobileComponent', () => {
  let component: MobileComponent;
  let fixture: ComponentFixture<MobileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [MobileComponent],
      imports: [MatIconModule,
        RouterTestingModule,
        MatSnackBarModule,
        HttpClientTestingModule]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MobileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
