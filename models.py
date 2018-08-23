class ThreadSafeTestingModel(models.Model):
    MOCK_SAVE = False

    # first time we need to save regularly to avoid populating auto fields / pk etc.
    first_save = False

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        force_update = 'force_update' in kwargs and kwargs['force_update']
        if UNIT_TESTING and self.first_save and not force_update and ThreadSafeTestingModel.MOCK_SAVE:
            return
        self.first_save = True
        super(ThreadSafeTestingModel, self).save(*args, **kwargs)

    def refresh_from_db(self, **kwargs):
        if UNIT_TESTING and ThreadSafeTestingModel.MOCK_SAVE:
            return
        super(ThreadSafeTestingModel, self).refresh_from_db(**kwargs)

