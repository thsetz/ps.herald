describe('ps-herald-angular App', function() {
  it('should have a title', function() {
    //browser.waitForAngularEnabled(false);
    //browser.get('http://localhost:5000/');
    browser.get('http://localhost:4200/');
    expect(browser.getTitle()).toEqual('PsHeraldAngular');
  }); 
});

