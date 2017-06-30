require 'yaml'

class PersistedYaml
  FILE_NAME = "wavegbuildings.yml"

  attr_accessor :yaml

  def initialize
    @yaml = read_existing
  end

  def read_existing
    YAML.load_file("#{FILE_NAME}")
  end

  def add(entry)
    if yaml["building_urls"].nil?
      yaml["building_urls"] = []
    end
    yaml["building_urls"] << "http://#{entry}"
  end

  def write_update
    File.open(FILE_NAME, 'w') {|f| f.write(yaml.to_yaml)}
  end
end