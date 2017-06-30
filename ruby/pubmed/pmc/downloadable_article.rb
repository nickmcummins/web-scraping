module DownloadableArticle
  def article_name
    raise NotImplementedError
  end

  def article_local_directory
    home_dir = ENV["HOME"]
    "#{home_dir}/Articles/pmc/#{article_name}"
  end

  def article_local_filename(ext)
    "#{article_local_directory}/#{article_name}.#{ext}"
  end
end