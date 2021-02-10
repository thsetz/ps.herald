import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CmessagesComponent } from './cmessages.component';

describe('CmessagesComponent', () => {
  let component: CmessagesComponent;
  let fixture: ComponentFixture<CmessagesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CmessagesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CmessagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
