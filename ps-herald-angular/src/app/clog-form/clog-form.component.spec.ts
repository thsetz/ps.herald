import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClogFormComponent } from './clog-form.component';

describe('ClogFormComponent', () => {
  let component: ClogFormComponent;
  let fixture: ComponentFixture<ClogFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ClogFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ClogFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
