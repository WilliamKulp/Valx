column_search_term_mapping = {
    "keyword_search":{
        				"search_type":"free_text",
        				"features":
    	    				{"nct_id":{
    	                                "null_val":free_text_null_value,
    	                                    },
    	                      "original_study_id":{
    	                                "null_val":free_text_null_value
    	                                    },
    	                      "brief_title":{
    	                                "null_val":free_text_null_value
    	                                    },
    	                      "official_title":{
    	                                "null_val":free_text_null_value
    	                                    },
    	                      "brief_summary":{
    	                                "null_val":free_text_null_value
    	                                    },
    	                      "detailed_description":{
    	                                "null_val":free_text_null_value
    	                                    },
    	                     "secondary_id":{
    	                                "null_val":free_text_null_value
    	                                    }#,
    	                      # "condition":{
    	                      #           "null_val":free_text_null_value
    	                      #               },
    	                      # "trial_keywords":{
    	                      #           "null_val":free_text_null_value
    	                      #               }
    	                    }
                      },
	"indication_search":{
        				"search_type":"free_text",
        				"features":{
		                      "brief_title":{
		                                "null_val":free_text_null_value
		                                    },
		                      "official_title":{
		                                "null_val":free_text_null_value
		                                    },
		                      "brief_summary":{
		                                "null_val":free_text_null_value
		                                    }#,
		                      # "condition":{
		                      #           "null_val":free_text_null_value
		                      #               },
		                      # "trial_keywords":{
		                      #           "null_val":free_text_null_value
		                      #               }
		                            }        
                        },
	"investigational_product":{
		        				"search_type":"free_text",
		        				"features":{
					                      "experimental_arm":{
					                                "null_val":free_text_null_value
					                                    },
					                      "official_title":{
					                                "null_val":free_text_null_value
					                                    },
					                      "trial_keywords":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
			                			
								},

	"sponsor_class":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "sponsor_class":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
			                			
					},

	"sponsor_name":{
		        				"search_type":"free_text",
		        				"features":{
					                      "sponsor_name":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
					},

	"global_flag":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "global_flag":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
					},
	"trial_status":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "overall_status":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
					},

	"trial_phase":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "phase":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
					},

	"study_type":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "study_type":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
					},

	"results_available":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "results_available":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
					},

	"publication_available":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "publication_available":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
					},

	"start_year":{
		        				"search_type":"range_filter",
		        				"features":{
					                      "start_year":{
					                                "null_val":start_year_null_val,
					                                "filter":"gte"
					                                    }
					                        }
					},
	"end_year":{
		        				"search_type":"range_filter",
		        				"features":{
					                      "end_year":{
					                                "null_val":end_year_null_val,
		        									"filter":"lte"
					                                    }
					                        }
					},

	"line_of_therapy":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "LoT":{
					                                "null_val":free_text_null_value

					                                    }
					                        }
					},

	"metastasis_flag":{
		        				"search_type":"filter_match",
		        				"features":{
					                      "meta":{
					                                "null_val":free_text_null_value
					                                    }
					                        }
					},
    "negations":{
		        				"search_type":"free_text",
		        				"features":{
					                      "negations_dep":{
					                                "null_val":free_text_null_value # ensure null check is successful.Else might not index as list
					                                    },
					                      "negations_negex":{
					                                "null_val":free_text_null_value # ensure null check is successful.Else might not index as list
					                                    }
					                        }
					}
	}