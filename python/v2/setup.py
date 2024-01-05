from setuptools import setup, find_packages

setup(name="python_perform_host_performance",
      version="0.2.13",
      description="Python_perform_host_performance python EF2 extension",
      author="Dynatrace",
      packages=find_packages(),
      python_requires=">=3.10",
      include_package_data=True,
      install_requires=[
            "dt-extensions-sdk",
            "psutil>=5.9.6"],
      extras_require={"dev": ["dt-extensions-sdk[cli]"]},
      )
