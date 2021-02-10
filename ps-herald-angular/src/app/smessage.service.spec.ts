import { TestBed } from '@angular/core/testing';

import { SmessageService } from './smessage.service';

describe('SmessageService', () => {
  let service: SmessageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SmessageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
