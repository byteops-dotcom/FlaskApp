document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.querySelector('.theme-toggle');
  const savedTheme = window.localStorage.getItem('task-forge-theme');
  const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches;

  function setTheme(isDark) {
    document.documentElement.classList.toggle('dark-mode', isDark);
    document.body.classList.toggle('dark-mode', isDark);
    if (themeToggle) {
      themeToggle.setAttribute('aria-pressed', String(isDark));
      themeToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      themeToggle.querySelector('.theme-label').textContent = isDark ? 'Light mode' : 'Dark mode';
    }
  }

  setTheme(savedTheme ? savedTheme === 'dark' : Boolean(prefersDark));
  themeToggle?.addEventListener('click', () => {
    const isDark = !document.documentElement.classList.contains('dark-mode');
    setTheme(isDark);
    window.localStorage.setItem('task-forge-theme', isDark ? 'dark' : 'light');
  });

  document.querySelectorAll('.flash').forEach((flash) => {
    window.setTimeout(() => {
      flash.style.opacity = '0';
      flash.style.transform = 'translateY(-6px)';
      flash.style.transition = 'opacity .3s, transform .3s';
      window.setTimeout(() => flash.remove(), 300);
    }, 5000);
  });

  const search = document.querySelector('#task-search');
  const taskItems = [...document.querySelectorAll('.task-item')];
  const noResults = document.querySelector('.no-results');
  let activeFilter = 'all';

  function filterTasks() {
    const query = (search?.value || '').trim().toLowerCase();
    let visible = 0;
    taskItems.forEach((task) => {
      const matchesFilter = activeFilter === 'all' || task.dataset.status === activeFilter;
      const matchesSearch = task.dataset.title.includes(query);
      task.classList.toggle('is-hidden', !(matchesFilter && matchesSearch));
      if (matchesFilter && matchesSearch) visible += 1;
    });
    if (noResults) noResults.hidden = visible !== 0;
  }

  search?.addEventListener('input', filterTasks);
  document.querySelectorAll('.filter-pill').forEach((pill) => {
    pill.addEventListener('click', () => {
      activeFilter = pill.dataset.filter;
      document.querySelectorAll('.filter-pill').forEach((item) => item.classList.remove('active'));
      pill.classList.add('active');
      filterTasks();
    });
  });

  document.querySelectorAll('.edit-button').forEach((button) => {
    button.addEventListener('click', () => {
      const item = button.closest('.task-item');
      item.classList.add('is-editing');
      item.querySelector('.edit-form input').focus();
      item.querySelector('.edit-form input').select();
    });
  });
});
