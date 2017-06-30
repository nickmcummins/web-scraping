require 'selenium-webdriver'
require '../googlesearch/persisted_yaml'

class WaveGBuildingGoogleSearchResult
  BASE_URL = "https://www.google.com/search?q=site:waveg.wavebroadband.com/building"

  attr_reader :urls, :driver, :persisted_yaml

  def initialize(page, persisted_yaml = PersistedYaml.new)
    @urls = generate_urls(page)
    @driver = build_driver
    @persisted_yaml = persisted_yaml
  end


  def generate_urls(pages)
    urls = []
    pages.each do |page|
      start_index = (page - 1) * 10
      urls << "#{BASE_URL}&start=#{start_index}"
    end
    urls
  end

  def build_driver
    Selenium::WebDriver.for :chrome
  end

  def load_and_retrieve
    urls.each do |url|
      driver.navigate.to(url)
      building_urls.each{|url| persisted_yaml.add(url)}
    end
    persisted_yaml.write_update
    driver.close
  end

  def building_urls
    result_urls = driver.find_elements(:class => '_Rm')
    result_urls.map{|result| result.text}
  end

  def close
    driver.quit
  end
end


wavegbuilding_googlesearchresultset = WaveGBuildingGoogleSearchResult.new((1..7).to_a)
wavegbuilding_googlesearchresultset.load_and_retrieve
