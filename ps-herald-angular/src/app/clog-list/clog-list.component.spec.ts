import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClogListComponent } from './clog-list.component';

describe('ClogListComponent', () => {
  let component: ClogListComponent;
  let fixture: ComponentFixture<ClogListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ClogListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ClogListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
