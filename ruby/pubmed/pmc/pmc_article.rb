require 'selenium-webdriver'
require 'fileutils'
require './downloadable_article'

class PMCArticle
  include DownloadableArticle

  @@articles_dir = '/home/nick/Articles/pmc'

  attr_reader :url, :driver, :article_name

  def initialize(url)
    @url = url
    @driver = build_driver
    @article_name = open
  end

  def build_driver
    prefs = {
        :download => {
            :prompt_for_download => false,
            :default_directory => "/home/nick/Articles/pmc/tmp"
        }
    }
    Selenium::WebDriver.for :chrome, :prefs => prefs
  end

  def open
    driver.navigate.to url
    content_title
  end

  def content_title
    content_title = driver.find_element(:class, 'content-title').text
    content_title.gsub(/[\s\:]+/, '-')
  end

  def download_epub
    epub_link = driver.find_element(:class, 'epub-link')
    epub_link.click
    download_article_btn = driver.find_element(:id, 'downloadEpub')
    download_article_btn.click

    article_name = content_title
    FileUtils.mkdir(article_name) unless File.directory?(article_local_directory)

    moved_file = false
    until moved_file do
      epub_files = (Dir.entries("/home/nick/Articles/pmc/tmp") - %w(. ..)).select{|file| is_downloaded_epub(file) }
      if !epub_files.empty?
        epub_file = epub_files.first
        FileUtils.move("/home/nick/Articles/pmc/tmp/" + epub_file, article_local_filename("epub"))
        moved_file = true
      end
      sleep 5
    end
  end

  def is_downloaded_epub(file)
    file.include?(".epub") && !file.include?("crdownload") && !file.include?("tmp")
  end


  def close
    driver.quit
  end
end

pmc_article = PMCArticle.new('http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4878959/')
pmc_article.download_epub
pmc_article.close