import { TestBed } from '@angular/core/testing';

import { SlogDataService } from './slog-data.service';

describe('SlogDataService', () => {
  let service: SlogDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SlogDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
