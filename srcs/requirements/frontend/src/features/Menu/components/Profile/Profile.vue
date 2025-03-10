<template>
  <div class="profile">
    <div class="profile__details">
      <div class="profile__avatar-container">
        <component
          :is="svgComponents['PersonIcon']"
          v-if="isVueComponent(svgComponents['PersonIcon'])"
          class="profile__avatar-icon"
        />
      </div>
      <div class="profile__person-details">
        <p class="profile__username">{{ userInfo?.username }}</p>
        <p>{{ userInfo?.email }}</p>
      </div>
    </div>
    <MyButton
      class-name="profile__button"
      type="button"
      color="secondary"
      :loading="isLoading"
      @click="handleSignOut"
      >{{ t('auth.signout.title') }}</MyButton
    >
  </div>
</template>

<script setup>
import { MyButton } from 'components';
import usersApi from 'entities/Users/api';
import authApi from 'shared/api/Auth';
import { useQuery } from 'shared/composables';
import { useMutation } from 'shared/composables';
import { isVueComponent, svgComponents } from 'shared/lib';
import { auth } from 'store/auth.js';
import { inject } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

const { t } = useI18n();
const router = useRouter();
const showErrorModal = inject('showErrorModal');
const notify = inject('notify');

const { data: userInfo = {} } = useQuery(usersApi.getUserInfo, {
  select: (res) => res?.data,
  onError: (error) => {
    const errorMessage =
      error?.response?.data?.message || error?.response?.statusText || t('unknown_error');
    showErrorModal(error.status, errorMessage);
  },
});

const { mutate: onSignOut, isLoading } = useMutation(authApi.signOut, {
  onSuccess: () => {
    auth.logout();
    notify(t('success', 'success'));
    router.push('/signin');
  },
  onError: (error) => {
    const errorMessage =
      error?.response?.data?.message || error?.response?.statusText || t('unknown_error');
    showErrorModal(error.status, errorMessage);
  },
});

const handleSignOut = (event) => {
  event.stopPropagation();
  onSignOut();
};
</script>

<style scoped>
.profile {
  display: flex;
  flex-direction: row;
  column-gap: var(--big-space);
  justify-content: space-between;

  width: 100%;
}

.profile__details {
  display: flex;
  flex-direction: row;
  column-gap: var(--regular-space);
}

.profile__avatar-container {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 90px;
  height: 90px;

  background-color: var(--light-color);
  border-radius: 50%;
}

.profile__avatar-icon {
  transform: translate(-1px, -1px);
  width: 90px;
  height: 90px;
}

.profile__person-details {
  display: flex;
  flex-direction: column;
  row-gap: var(--small-space);
}

.profile__username {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--secondary-color);
}

::v-deep(.profile__button) {
  max-height: 44px;
}
</style>
